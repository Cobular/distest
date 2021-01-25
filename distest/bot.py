""" Contains the discord clients used to run tests.

:py:class:`DiscordBot` contains the logic for running tests and finding the target bot

:py:class:`DiscordInteractiveInterface` is a subclass of :py:class:`DiscordBot` and contains the logic to handle
commands sent from discord to run tests, display stats, and more

:py:class:`DiscordCliInterface` is a subclass of :py:class:`DiscordInteractiveInterface` and simply contains logic to
start the bot when it wakes up
"""

import discord

from .TestInterface import TestResult, Test, TestInterface
from .exceptions import TestRequirementFailure
from .collector import TestCollector

HELP_TEXT = """\
**::help** - Show this help
**::run** all - Run all tests
**::run** unrun - Run all tests that have not been run
**::run** *name* - Run a specific test
**::list** - List all the tests and their status
"""

intents = discord.Intents.default()
intents.members = True
intents.presences = True


class DiscordBot(discord.Client):
    """ Discord bot used to run tests.
    This class by itself does not provide any useful methods for human interaction,
    and is just used as a superclass of the two interfaces,
    :py:class:`DiscordInteractiveInterface` and :py:class:`DiscordCliInterface`

    :param str target_id: The name of the target bot, used to ensure that the target user is actually
                            present in the server. Good for checking for typos or other simple mistakes.
    """

    def __init__(self, target_id):
        super().__init__(intents=intents)
        self._target_name = target_id

    def _find_target(self, server: discord.Guild) -> discord.Member:
        """ Confirms that the target user is actually present in the specified guild

            :param discord.Guild server: The ``discord.Guild()`` object of the guild
            to look for the target user in
            :rtype:  discord.Member
        """
        for member in server.members:
            if self._target_name == member.id:
                if member.status == discord.Status.offline:
                    print("Looks like the target bot is on the server but offline, "
                          "you might want to check on that!")
                return member
        print("Looks like I can't see any server members! You may need to enable the privileged gateway intent, see "
              "here for how to do so: https://discordpy.readthedocs.io/en/latest/intents.html")
        raise KeyError("Could not find member with id {}".format(self._target_name))

    async def run_test(
            self, test: Test, channel: discord.TextChannel, stop_error=False
    ) -> TestResult:
        """ Run a single test in a given channel.

            Updates the test with the result and returns it

            :param Test test: The :py:class:`Test <distest.TestInterface.Test>` that is to be run
            :param discord.TextChannel channel: The
            :param stop_error: Weather or not to stop the program on error. Not currently in use.
            :return: Result of the test
            :rtype: TestResult
        """
        test_interface = TestInterface(self, channel, self._find_target(channel.guild))
        try:
            print("Running test: {}".format(test.name))
            await test.func(test_interface)
        except TestRequirementFailure:
            test.result = TestResult.FAILED
            if not stop_error:
                raise
        else:
            test.result = TestResult.SUCCESS
        return test.result


class DiscordInteractiveInterface(DiscordBot):
    """ A variant of the discord bot which commands sent in discord to allow
    a human to run the tests manually.

    Does NOT support CLI arguments

    :param str target_id: The name of the bot to target (Username, no discriminator)
    :param TestCollector collector: The instance of Test Collector that contains the tests to run
    :param int timeout: The amount of time to wait for responses before failing tests.
    """

    def __init__(self, target_id, collector: TestCollector, timeout=5):
        super().__init__(target_id)
        self._tests = collector
        self.timeout = timeout
        self.failure = False

    async def _run_by_predicate(self, channel, predicate=lambda test: True):
        """ Iterate through ``_tests`` and run any test for which ``predicate`` returns True

        :param discord.TextChannel channel: The channel to run the test in.
        :param function predicate: The check a test must pass to be run.
        """
        for test in self._tests:
            if predicate(test):
                await self.run_test(test, channel, stop_error=True)

    async def _build_stats(self, tests) -> str:
        """ Helper function for constructing the stat display based on test status.
        Iterate over each test in ``tests`` and creates a string (``response``) based
        on the result property of each ``Test``

        :param list[Test] tests: The list of tests used to create the stats
        :return: Ready-to-send string congaing the results of the tests, including
                 discord markdown
        :rtype: str
        """
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
                response += "✓ Passed\n"
            elif test.result is TestResult.FAILED:
                response += "✘ Failed\n"
                self.failure = True
        response += "```\n"
        return response

    async def _display_stats(self, channel: discord.TextChannel):
        """ Display the status of the various tests. Just a send wrapper for
        :py:func:`_build_stats`
        """
        await channel.send(await self._build_stats(self._tests))

    async def on_ready(self):
        """ Report when the bot is ready for use and report the available tests
        to the console
        """
        print("Started distest bot.")
        print(f"Invite Link: https://discordapp.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=8 ")
        print("Available tests are:")
        for test in self._tests:
            print("   {}".format(test.name))

    async def on_message(self, message: discord.Message):
        """ Handle an incoming message, see :py:func:`discord.event.on_message` for
        event reference.

        Parse a message, can ignore it or parse the message as a command and
        run some tests or do one of the alternate functions (stats, list, or help)

        :param discord.Message message: The message being recieved, passed by discord.py
        """
        if message.author == self.user:
            return
        if not isinstance(message.channel, (discord.DMChannel, discord.GroupChannel)):
            if message.content.startswith("::run "):
                name = message.content[6:]
                await self.run_tests(message.channel, name)
                await self._display_stats(message.channel)
            elif message.content in ["::stats", "::list"]:
                await self._display_stats(message.channel)
            elif message.content == "::help":
                await message.channel.send(HELP_TEXT)

    async def run_tests(self, channel: discord.TextChannel, name: str):
        """ Helper function for choosing and running an appropriate suite of tests
        Makes sure only tests that still need to be run are run, also prints
        to the console when a test is run

        :param discord.TextChannel channel: The channel in which to run the tests
        :param str name: Selector string used to determine what category of test to run
        """
        print("Running: ", name)
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
            await channel.send(channel, text.format(name))
        else:
            print("Running test: {}".format(name))
            await self.run_test(self._tests.find_by_name(name), channel)


class DiscordCliInterface(DiscordInteractiveInterface):
    """ A variant of the discord bot which is designed to be run off command line arguments.

    :param str target_id: The name of the bot to target (Username, no discriminator)
    :param TestCollector collector: The instance of Test Collector that contains the
                                    tests to run
    :param str test: The name of the test option (all, specific test, etc)
    :param int channel_id: The ID of the channel to run the bot in
    :param bool stats: If true, run in hstats mode.
    """

    def __init__(self, target_id, collector, test, channel_id, stats, timeout):
        super().__init__(target_id, collector, timeout)
        self._test_to_run = test
        self._channel_id = channel_id
        self._stats = stats
        self._channel = None

    def run(self, token) -> int:
        """ Override of the default run() that returns failure state after completion.
        Allows the failure to cascade back up until it is processed into an exit code by
        :py:func:`run_command_line_bot`

        :param str token: The tester bot token
        :return: Returns 1 if the any test failed, otherwise returns zero.
        :rtype: int
        """
        super().run(token)
        return self.failure

    async def on_ready(self):
        """ Run all the tests sequentially when the bot becomes awake and exit when the
        tests finish. The CLI should run all by itself without prompting, and this allows it
        to behave that way.
        """
        self._channel = self.get_channel(self._channel_id)
        print("Started distest bot.")
        print(f"Invite Link: https://discordapp.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=8 ")
        if self._test_to_run is not None:
            await self.run_tests(self._channel, self._test_to_run)
            await self._display_stats(self._channel)
        elif self._stats:
            await self._display_stats(self._channel)
        await self.close()
