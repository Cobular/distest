""" Distest is a small library designed to help with the
    creation of bots to test other bots. This is currently
    part of the MathBot project but if it gains enough
    traction I might fork it into its own repository
    Interfacing with the bot through discord:

    ::stats
        Gives details about which tests have been
        run and what the results were

    ::run test_name
        Run a particular test

    ::run all
        Run all tests

    ::run unrun
        Run all tests that have not yet been run

    ::run failed
        Run all tests that failed on the most recent run

"""

import argparse
import asyncio
import enum
import re
from sys import exit
from concurrent.futures import _base

import discord

TIMEOUT = 5
# The exit code will be stored here when the program exits, this can be handled in the tester bot
# after run() finished
EXIT_CODE = 0

HELP_TEXT = """\
**::help** - Show this help
**::run** all - Run all tests
**::run** unrun - Run all tests that have not been run
**::run** *name* - Run a specific test
**::list** - List all the tests and their status
"""

SPECIAL_TEST_NAMES = {"all", "unrun", "failed"}


class TestRequirementFailure(Exception):
    """ Base class for the errors that are raised when an expectation is not met """


class NoResponseError(TestRequirementFailure):
    """ Raised when the target bot fails to respond to a message """


class NoReactionError(TestRequirementFailure):
    """ Raised when the target bot failed to react to a message """


class UnexpectedResponseError(TestRequirementFailure):
    """ Raised when the target bot failed to stay silent """


class ErrordResponseError(TestRequirementFailure):
    """ Raised when the target bot produced an error message """


class UnexpectedSuccessError(TestRequirementFailure):
    """ Raised when the target bot failed to produce an error message """


class HumanResponseTimeout(TestRequirementFailure):
    """ Raised when a human fails to assert the result of a test """


class HumanResponseFailure(TestRequirementFailure):
    """ Raised when a human fails a test """


class ResponseDidNotMatchError(TestRequirementFailure):
    """ Raised when the target bot responds with a message that doesn't meet criteria """


class ReactionDidNotMatchError(TestRequirementFailure):
    """ Raised when the target bot reacts with the wrong emoji """


class TestResult(enum.Enum):
    """ Enum representing the result of running a test case """

    UNRUN = 0
    SUCCESS = 1
    FAILED = 2


class Test:
    """ Holds data about a specific test """

    def __init__(self, name: str, func, needs_human: bool = False) -> None:
        if name in SPECIAL_TEST_NAMES:
            raise ValueError("{} is not a valid test name".format(name))
        self.name = name  # The name of the test
        self.func = func  # The function to run when running the test
        self.last_run = 0  # When the test was last run
        self.result = (
            TestResult.UNRUN
        )  # The result of the test (True or False) or None if it was not run
        self.needs_human = needs_human  # Whether the test requires human interation


class Interface:
    """ The interface that the test functions should use to interface with discord.
        Test functions should not access the discord.py client directly.
    """

    def __init__(
        self,
        client: discord.Client,
        channel: discord.TextChannel,
        target: discord.Member,
    ) -> None:
        self.client = client  # The discord.py client object
        self.channel = channel  # The channel the test is running in
        self.target = target  # The bot which we are testing

    async def send_message(self, content):
        """ Send a message to the testing channel. """
        return await self.channel.send(content)

    @staticmethod
    async def edit_message(message: discord.Message, new_content):
        """ Modified a message. Doesn't actually care what this message is. """
        return await message.edit(content=new_content)

    async def wait_for_reaction(self, message: discord.Message):
        """ Tests to make sure a message is reacted to.

        Requires a discord.py Message as input to run,
        so this is not meant to be run by the user dirrectly in most cases.
        """

        def check(reaction, user):
            return (
                reaction.message.id == message.id
                and user == self.target
                and reaction.message.channel == self.channel
            )

        try:
            result = await self.client.wait_for(
                "reaction_add", timeout=TIMEOUT, check=check
            )
        except _base.TimeoutError:
            raise NoReactionError
        else:
            return result

    async def wait_for_message(self):
        """ Waits for the bot the send a message.
            If the bot takes longer than 20 seconds (Default, configurable with , TIMEOUT) the test fails.
        """

        def check(message: discord.Message):
            return message.channel == self.channel and message.author == self.target

        try:
            result = await self.client.wait_for("message", timeout=TIMEOUT, check=check)
        except _base.TimeoutError:
            raise NoResponseError
        else:
            return result

    async def wait_for_reply(self, content):
        """ Sends a message and returns the next message that the targeted bot sends. """
        await self.channel.send(content)
        return await self.wait_for_message()

    async def assert_message_equals(self, matches):
        """ Waits for the next message.
            If the message does not match a string exactly, fail the test.
        """
        response = await self.wait_for_message()
        if response.content != matches:
            raise ResponseDidNotMatchError
        return response

    async def assert_message_contains(self, substring):
        """ Waits for the next message.
            If the message does not contain the given substring, fail the test.
        """
        response = await self.wait_for_message()
        if substring not in response.content:
            raise ResponseDidNotMatchError
        return response

    async def assert_message_matches(self, regex):
        """ Waits for the next message.
            If the message does not match a regex, fail the test.
        """
        response = await self.wait_for_message()
        if not re.match(regex, response.content):
            raise ResponseDidNotMatchError
        return response

    async def assert_reply_equals(self, contents: str, matches: str):
        """ Send a message and wait for a response.
            If the response does not match a string exactly, fail the test.
        """
        # print('Sending...')
        await self.send_message(contents)
        # print('About to wait...')
        response = await self.wait_for_message()
        # print('Got response')
        if response.content != matches:
            raise ResponseDidNotMatchError
        return response

    async def assert_reply_contains(self, contents: str, substring: str):
        """ Send a message and wait for a response.
            If the response does not contain the given substring, fail the test.
        """
        await self.send_message(contents)
        response = await self.wait_for_message()
        if substring not in response.content:
            raise ResponseDidNotMatchError
        return response

    async def assert_reply_matches(self, contents: str, regex):
        """ Send a message and wait for a response. If the response does not match a regex, fail the test.

            Requires a properly formatted Python regex ready to be used in the re functions.
        """
        await self.send_message(contents)
        response = await self.wait_for_message()
        if not re.match(regex, response.content):
            raise ResponseDidNotMatchError
        return response

    async def assert_reaction_equals(self, contents, emoji):
        reaction = await self.wait_for_reaction(await self.send_message(contents))
        if str(reaction[0].emoji) != emoji:
            raise ReactionDidNotMatchError
        return reaction

    async def ensure_silence(self):
        """ Ensures that the bot does not post any messages for some number of seconds. """

        def check(message: discord.Message):
            return message.channel == self.channel and message.author == self.target

        try:
            await self.client.wait_for("message", timeout=TIMEOUT, check=check)
        except _base.TimeoutError:
            pass
        else:
            raise UnexpectedResponseError

    async def ask_human(self, query):
        """ Asks a human for an opinion on a question. Currently, only yes-no questions
            are supported. If the human answers 'no', the test will be failed.
        """
        message = await self.channel.send(query)
        await message.add_reaction(
            "\u2714"
        )  # TODO: Check to make sure the emoji work right in this form
        await message.add_reaction("\u274C")
        await asyncio.sleep(0.5)

        def check(human_reaction, user):
            return human_reaction.message

        try:
            reaction: discord.Reaction = await self.client.wait_for(
                "reaction_add", timeout=TIMEOUT, check=check
            )
            # TODO: Confirm this BS works in place of a check function
        except _base.TimeoutError:
            raise HumanResponseTimeout
        else:
            reaction, _ = reaction
            if reaction.emoji == "\u274C":
                raise HumanResponseFailure


class ExpectCalls:
    """ Wrap a function in an object which counts the number
        of times it was called. If the number of calls is not
        equal to the expected number when this object is
        garbage collected, something has gone wrong, and in
        that case an error is thrown.
    """

    def __init__(self, function, expected_calls=1):
        self.function = function
        self.expected_calls = expected_calls
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        return self.function(*args, **kwargs)

    def __del__(self):
        if self.call_count != self.expected_calls:
            message = (
                "{} was called {} times. It was expected to have been called {} times"
            )
            raise RuntimeError(
                message.format(self.function, self.call_count, self.expected_calls)
            )


class TestCollector:
    """ Used to group tests and pass them around all at once. """

    def __init__(self):
        self._tests = []

    def add(self, function, name: str = "", needs_human: bool = False):
        """ Adds a test function to the group. """
        name = name or function.__name__
        test = Test(name, function, needs_human=needs_human)
        if name in self._tests:
            raise KeyError("A test case called {} already exists.".format(name))
        self._tests.append(test)

    def find_by_name(self, name: str):
        """ Return the test with the given name.
            Return None if it does not exist.
        """
        for i in self._tests:
            if i.name == name:
                return i
        return None

    def __call__(self, *args, **kwargs):
        """ Add a test decorator-style. """

        def _decorator(function):
            self.add(function, *args, **kwargs)

        return ExpectCalls(_decorator, 1)

    def __iter__(self):
        return (i for i in self._tests)


class DiscordBot(discord.Client):
    """ Discord bot used to run tests.
        This class by itself does not provide any useful methods for human interaction.
    """

    def __init__(self, target_name: str) -> None:
        super().__init__()
        self._target_name = target_name.lower()

    # s self._setup_done = False

    def _find_target(self, server: discord.Guild) -> discord.Member:
        for i in server.members:
            if self._target_name in i.name.lower():
                return i
        raise KeyError("Could not find memory with name {}".format(self._target_name))

    async def run_test(
        self, test: Test, channel: discord.TextChannel, stop_error: bool = False
    ) -> TestResult:
        """ Run a single test in a given channel.
            Updates the test with the result, and also returns it.
        """
        interface = Interface(self, channel, self._find_target(channel.guild))
        try:
            await test.func(interface)
        except TestRequirementFailure:
            test.result = TestResult.FAILED
            if not stop_error:
                raise
        else:
            test.result = TestResult.SUCCESS
        return test.result

    async def fail_close(self, failure):
        global EXIT_CODE
        if failure:
            EXIT_CODE = 1
        else:
            EXIT_CODE = 0
        await super().close()


class DiscordInteractiveInterface(DiscordBot):
    """
    A variant of the discord bot which supports additional commands in discord
    to allow a human to run the tests manually. Does NOT support CLI commands


    :param target_name: The name of the bot to target (Username, no discriminator)
    :param tests: The instance of Test Collector that contains the tests to run
    """

    def __init__(self, target_name: str, tests: TestCollector) -> None:
        super().__init__(target_name)
        self._tests = tests

    async def _run_by_predicate(self, channel, predicate):
        for test in self._tests:
            if predicate(test):
                await channel.send("**Running test {}**".format(test.name))
                await self.run_test(test, channel, stop_error=True)

    async def _display_stats(self, channel: discord.TextChannel) -> None:
        """ Display the status of the various tests. """
        # NOTE: An emoji is the width of two spaces
        response = "```\n"
        longest_name = max(map(lambda t: len(t.name), self._tests))
        for test in self._tests:
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
        response += "```\n"
        await channel.send(response)

    async def on_ready(self) -> None:
        """ Report when the bot is ready for use """
        print("Started distest bot.")
        print("Available tests are:")
        for i in self._tests:
            print("   {}".format(i.name))

    async def on_message(self, message: discord.Message) -> None:
        """ Handle an incoming message """
        if message.author == self.user:
            return
        if not isinstance(message.channel, (discord.DMChannel, discord.GroupChannel)):
            if message.content.startswith("::run "):
                name = message.content[6:]
                print("Running test:", name)
                if name == "all":
                    await self._run_by_predicate(message.channel, lambda t: True)
                    await self._display_stats(message.channel)
                elif name == "unrun":

                    def pred(t):
                        return t.result is TestResult.UNRUN

                    await self._run_by_predicate(message.channel, pred)
                    await self._display_stats(message.channel)
                elif name == "failed":

                    def pred(t):
                        return t.result is TestResult.FAILED

                    await self._run_by_predicate(message.channel, pred)
                    await self._display_stats(message.channel)
                # TODO: Fix this, but what was it supposed to be?
                # elif '*' in name:
                #    regex = re.compile(name.replace('*', '.*'))
                #    await self.run_many(message, lambda t: regex.fullmatch(t.name))
                elif self._tests.find_by_name(name) is None:
                    text = ":x: There is no test called `{}`"
                    await message.channel.send(message.channel, text.format(name))
                else:
                    await message.channel.send("Running test `{}`".format(name))
                    await self.run_test(self._tests.find_by_name(name), message.channel)
                    await self._display_stats(message.channel)
            # Status display command
            elif message.content in ["::stats", "::list"]:
                await self._display_stats(message.channel)
            elif message.content == "::help":
                await message.channel.send(HELP_TEXT)


class DiscordCliInterface(DiscordBot):
    """ A variant of the discord bot which is designed to be run off command line arguments.

    :param target_name: The name of the bot to target (Username, no discriminator)
    :param tests: The instance of Test Collector that contains the tests to run
    :param test: The name of the test option (all, specific test, etc)
    :param channel_id: The ID of the channel to run the bot in
    :param stats: If true, run in stats mode. TODO: See if this is actually useful
    """

    def __init__(
        self,
        target_name: str,
        tests: TestCollector,
        test: str,
        channel_id: int,
        stats: bool,
    ) -> None:
        super().__init__(target_name)
        self._tests = tests
        self._test_to_run = test
        self._channel_id = channel_id
        self._stats = stats
        self._channel = None

    async def _run_by_predicate(self, channel, predicate):
        for test in self._tests:
            if predicate(test):
                await channel.send("**Running test {}**".format(test.name))
                await self.run_test(test, channel, stop_error=True)

    async def _display_stats(self, channel: discord.TextChannel) -> None:
        """
        Display the status of the various tests.

        Sets failure to true if any of the tests fail, then uses this to decide in the exit code.
        If no_exit is set to true, this will be ignored and it will not exit.
        Unrun will not result in a failure
        """
        failure = False
        # NOTE: An emoji is the width of two spaces
        response = "```\n"
        longest_name = max(map(lambda t: len(t.name), self._tests))
        for test in self._tests:
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
                failure = True  # A test failed, so the program should exit 1
        response += "```\n"
        await channel.send(response)

        # Controls the exit logic
        await self.fail_close(failure)

    async def on_ready(self) -> None:
        """ Report when the bot is ready for use """
        self._channel = self.get_channel(self._channel_id)
        print("Started distest bot.")
        print(f"Running test {self._test_to_run}")
        if self._test_to_run is not None:
            if self._test_to_run == "all":
                await self._run_by_predicate(self._channel, lambda t: True)
                await self._display_stats(self._channel)
            elif self._test_to_run == "unrun":

                def pred(t):
                    return t.result is TestResult.UNRUN

                await self._run_by_predicate(self._channel, pred)
                await self._display_stats(self._channel)
            elif self._test_to_run == "failed":

                def pred(t):
                    return t.result is TestResult.FAILED

                await self._run_by_predicate(self._channel, pred)
                await self._display_stats(self._channel)
            # TODO: Fix this, but what was it supposed to be?
            # elif '*' in self._test_to_run:
            #    regex = re.compile(self._test_to_run.replace('*', '.*'))
            #    await self.run_many(message, lambda t: regex.fullmatch(t.name))
            elif self._tests.find_by_name(self._test_to_run) is None:
                text = ":x: There is no test called `{}`"
                await self._channel.send(text.format(self._test_to_run))
            else:
                await self._channel.send("Running test `{}`".format(self._test_to_run))
                await self.run_test(
                    self._tests.find_by_name(self._test_to_run), self._channel
                )
                await self._display_stats(self._channel)
        elif self._stats:
            # Status display command
            await self._display_stats(self._channel)


def run_dtest_bot(sysargs, test_collector: TestCollector):
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
        global TIMEOUT
        TIMEOUT = clean_args.get("timeout")

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
        )
    else:
        print("Not in CLI mode")
        run_interactive_bot(
            clean_args.get("bot_target")[0],
            clean_args.get("bot_token")[0],
            test_collector,
        )


def run_interactive_bot(target_name, token, test_collector):
    bot: DiscordInteractiveInterface = DiscordInteractiveInterface(
        target_name, test_collector
    )
    bot.run(token)  # Starts the bot


def run_command_line_bot(target_name, token, run, channel_id, stats, test_collector):
    bot = DiscordCliInterface(target_name, test_collector, run, channel_id, stats)
    bot.run(token)
    exit(EXIT_CODE)
