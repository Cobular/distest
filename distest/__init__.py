""" Distest is a small library designed to allow you to make discord bots to test other bots.

    This is the main file, and contains the code that is directly involved in running the bot
    and interacting with the command line, including the classes for bot types and the two interfaces.
"""

import argparse
import sys

import discord

from .interface import TestResult, Test, TestInterface
from .exceptions import TestRequirementFailure
from .collector import ExpectCalls, TestCollector

HELP_TEXT = """\
**::help** - Show this help
**::run** all - Run all tests
**::run** unrun - Run all tests that have not been run
**::run** *name* - Run a specific test
**::list** - List all the tests and their status
"""


class DiscordBot(discord.Client):
    """ Discord bot used to run tests.
        This class by itself does not provide any useful methods for human interaction.
    """

    def __init__(self, target_name):
        super().__init__()
        self._target_name = target_name.lower()

    def _find_target(self, server: discord.Guild) -> discord.Member:
        for member in server.members:
            if self._target_name in member.name.lower():
                return member
        raise KeyError("Could not find memory with name {}".format(self._target_name))

    async def run_test(
        self, test: Test, channel: discord.TextChannel, stop_error=False
    ) -> TestResult:
        """ Run a single test in a given channel.
            Updates the test with the result, and also returns it.
        """
        test_interface = TestInterface(self, channel, self._find_target(channel.guild))
        try:
            await test.func(test_interface)
        except TestRequirementFailure:
            test.result = TestResult.FAILED
            if not stop_error:
                raise
        else:
            test.result = TestResult.SUCCESS
        return test.result


class DiscordInteractiveInterface(DiscordBot):
    """
    A variant of the discord bot which supports additional commands in discord
    to allow a human to run the tests manually. Does NOT support CLI commands


    :param str target_name: The name of the bot to target (Username, no discriminator)
    :param TestCollector collector: The instance of Test Collector that contains the tests to run
    """

    def __init__(self, target_name, collector: TestCollector, timeout=5):
        super().__init__(target_name)
        self._tests = collector
        self.timeout = timeout
        self.failure = False

    async def _run_by_predicate(self, channel, predicate=lambda test: True):
        for test in self._tests:
            if predicate(test):
                await channel.send("**Running test {}**".format(test.name))
                await self.run_test(test, channel, stop_error=True)

    async def _build_stats(self, tests) -> str:
        response = "```\n"
        longest_name = max(map(lambda t: len(t.name), tests))
        for test in tests:
            response += test.name.rjust(longest_name) + " "
            if test.needs_human:
                response += "✋ "
            else:
                response += "   "
            if test.result is TestResult.UNRUN:
                response += "⚫ Not run\n"
            elif test.result is TestResult.SUCCESS:
                response += "✔️ Passed\n"
            elif test.result is TestResult.FAILED:
                response += "❌ Failed\n"
                self.failure = True
        response += "```\n"
        return response

    async def _display_stats(self, channel: discord.TextChannel):
        """Display the status of the various tests."""
        await channel.send(await self._build_stats(self._tests))

    async def on_ready(self):
        """ Report when the bot is ready for use """
        print("Started distest bot.")
        print("Available tests are:")
        for test in self._tests:
            print("   {}".format(test.name))

    async def on_message(self, message: discord.Message):
        """ Handle an incoming message """
        if message.author == self.user:
            return
        if not isinstance(message.channel, (discord.DMChannel, discord.GroupChannel)):
            if message.content.startswith("::run "):
                name = message.content[6:]
                await self.run_tests(name)
                await self._display_stats(message.channel)
            elif message.content in ["::stats", "::list"]:
                await self._display_stats(message.channel)
            elif message.content == "::help":
                await message.channel.send(HELP_TEXT)

    async def run_tests(self, channel: discord.TextChannel, name: str):
        """ Helper function for choosing and running an appropriate suite of tests

            :param discord.TextChannel channel: The channel in which to run the tests
            :param str name: Selector string used to determine what category of test to run
        """
        print("Running test:", name)
        if name == "all":
            await self._run_by_predicate(channel)
        elif name == "unrun":
            await self._run_by_predicate(
                channel, lambda test: test.result is TestResult.UNRUN
            )
        elif name == "failed":
            await self._run_by_predicate(
                channel, lambda test: test.result is TestResult.FAILED
            )
        elif self._tests.find_by_name(name) is None:
            text = ":x: There is no test called `{}`"
            await channel.send(message.channel, text.format(name))
        else:
            await channel.send("Running test `{}`".format(name))
            await self.run_test(self._tests.find_by_name(name), channel)


class DiscordCliInterface(DiscordInteractiveInterface):
    """ A variant of the discord bot which is designed to be run off command line arguments.

    :param str target_name: The name of the bot to target (Username, no discriminator)
    :param TestCollector collector: The instance of Test Collector that contains the tests to run
    :param str test: The name of the test option (all, specific test, etc)
    :param int channel_id: The ID of the channel to run the bot in
    :param bool stats: If true, run in stats mode. TODO: See if this is actually useful
    """

    def __init__(
        self,
        target_name,
        collector: TestCollector,
        test: str,
        channel_id: int,
        stats: bool,
        timeout: int,
    ):
        super().__init__(target_name, collector, timeout)
        self._test_to_run = test
        self._channel_id = channel_id
        self._stats = stats
        self._channel = None

    # override of the default run() that returns failure state after completion.
    def run(self, token):
        super().run(token)
        return self.failure

    async def on_ready(self):
        """ For CLI, the bot should start testing as soon as its ready, and exit when it is done.
            Therefore, this ``on_ready`` does both.
        """
        self._channel = self.get_channel(self._channel_id)
        print("Started distest bot.")
        if self._test_to_run is not None:
            await self.run_tests(self._channel, self._test_to_run)
            await self._display_stats(self._channel)
        elif self._stats:
            await self._display_stats(self._channel)
        await self.close()


def run_dtest_bot(sysargs, test_collector: TestCollector, timeout=5):
    from distest.validate_discord_token import token_arg

    all_run_options = ["all"]
    for i in test_collector._tests:
        all_run_options.append(i.name)

    parser = argparse.ArgumentParser(
        description="A small library used to write automated unit tests for Discord bots. "
        "Has 2 modes, Interactive and CLI. "
        "If you include -c, the bot will expect to be used in CLI mode. "
        "See the github wiki for more info"
    )
    required = parser.add_argument_group("Always Required Arguments")
    required.add_argument(
        "bot_target",
        metavar="target_bot_user",
        type=str,
        nargs=1,
        help="The username of the target bot (not this bot). "
        "Remove the discriminant (#1234) so it is just the account's name.",
    )
    required.add_argument(
        "bot_token",
        metavar="tester_bot_token",
        type=token_arg,
        nargs=1,
        help="The bot token for the testing bot (this bot).",
    )
    cli_only = parser.add_argument_group("CLI Only")
    cli_only.add_argument(
        "--channel",
        "-c",
        metavar="channel",
        type=int,
        nargs=1,
        help="The channel ID that the tests should be occurring in (CLI) "
        "or the ID to send the awake message to (Interactive)",
        dest="channel",
    )
    run_stats_group = cli_only.add_mutually_exclusive_group()
    run_stats_group.add_argument(
        "--run",
        "-r",
        type=str,
        choices=all_run_options,
        help="Runs the bot in run mode, equivalent to ::run <option>. "
        "Options are listed, they are the tests declared in the bot and the three default options."
        "Required for the bot to be run in CLI mode, if using in Interactive mode, don't specify this",
    )
    run_stats_group.add_argument(
        "--stats",
        "-s",
        action="store_true",
        help="Runs the bot in stats mode, outputting the last runs stats. "
        "Equivalent to ::stats",
    )
    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        nargs=1,
        help="Changes the timeout (in seconds) on tests before they are assumed to have failed. "
        "Default is 5 sec.",
    )

    sysargs.pop(0)  # Pops off the first arg (the filename that is being run)
    clean_args = vars(parser.parse_args(sysargs))

    # Makes the changing of the timeout optional
    if clean_args.get("timeout") is not None:
        timeout = clean_args.get("timeout")[0]

    # Controls whether or not the bot is run in CLI mode based on the parameters present
    if clean_args["run"] is not None:
        # If --run is present, the bot should be in CLI mode
        print("In CLI mode")
        run_command_line_bot(
            clean_args.get("bot_target")[0],
            clean_args.get("bot_token")[0],
            clean_args.get("run"),
            clean_args.get("channel")[0],
            clean_args.get("stats"),
            test_collector,
            timeout,
        )
    else:
        print("Not in CLI mode")
        run_interactive_bot(
            clean_args.get("bot_target")[0],
            clean_args.get("bot_token")[0],
            test_collector,
            timeout,
        )


def run_interactive_bot(target_name, token, test_collector, timeout=5):
    bot: DiscordInteractiveInterface = DiscordInteractiveInterface(
        target_name, test_collector
    )
    bot.run(token)  # Starts the bot


def run_command_line_bot(target, token, tests, channel_id, stats, collector, timeout):
    """ Start the bot in command-line mode. The program will exit 1 if any of the tests failed.

        :param str target: The display name of the bot we are testing.
        :param str token: The tester's token, used to log in.
        :param str tests: List of tests to run.
        :param int channel_id: The ID of the channel in which to run the tests.
        :param bool stats: Determines whether or not to display stats after run.
        :param TestCollector collector: The ``TestCollector`` that gathered our tests.
        :param int timeout: The amount of time to wait for responses before failing tests.
        :rtype: None
    """
    bot = DiscordCliInterface(target, collector, tests, channel_id, stats, timeout)
    failed = bot.run(token)  # returns True if a test failed
    sys.exit(1 if failed else 0)
