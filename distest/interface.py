""" This file contains the tests the bot can run, as well as some supporting fluff.

Tests are within TestInterface(), please add more tests there.
"""

import enum
import asyncio
from concurrent.futures import _base
import re
import discord

from .exceptions import (
    TestRequirementFailure,
    NoResponseError,
    NoReactionError,
    UnexpectedResponseError,
    ErrordResponseError,
    UnexpectedSuccessError,
    HumanResponseTimeout,
    HumanResponseFailure,
    ResponseDidNotMatchError,
    ReactionDidNotMatchError,
)

SPECIAL_TEST_NAMES = {"all", "unrun", "failed"}


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


class TestInterface:
    """ All the tests, and some supporting functions.

        Tests are designed to be run by the tester bot and mixed together
        or with `send_message()` in order to actually test the bot.
    """

    def __init__(
        self,
        client: discord.Client,
        channel: discord.TextChannel,
        target: discord.Member,
    ):
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
                "reaction_add", timeout=self.client.timeout, check=check
            )
        except _base.TimeoutError:
            raise NoReactionError
        else:
            return result

    async def wait_for_message(self):
        """ Waits for the bot the send a message.
            If the bot takes longer than 5 seconds (default) the test fails.
        """

        def check(message: discord.Message):
            return message.channel == self.channel and message.author == self.target

        try:
            result = await self.client.wait_for(
                "message", timeout=self.client.timeout, check=check
            )
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

    async def assert_message_has_image(self, message: discord.Message):
        """ Assert ``message`` has an attachment. If not, fail the test."""
        if message.attachments is None:
            raise ResponseDidNotMatchError
        return message

    async def assert_reply_equals(self, contents: str, matches: str):
        """ Send a message and wait for a response.
            If the response does not match a string exactly, fail the test.
        """
        await self.send_message(contents)
        response = await self.wait_for_message()
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
        """ Send a message and wait for a response. If the response does not
            match a regex, fail the test. Requires a properly formatted Python regex
            ready to be used in the ``re`` functions.
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

    async def assert_reply_has_image(self, contents: str) -> discord.Message:
        """Send a message consisting of ``contents`` and wait for a reply.
           Check that the reply contains an attachment. If not, fail the test.
        """
        message = await self.wait_for_reply(contents)
        return await self.assert_message_has_image(message)

    async def ensure_silence(self):
        """ Ensures that the bot does not post any messages for some number of seconds. """

        def check(message: discord.Message):
            return message.channel == self.channel and message.author == self.target

        try:
            await self.client.wait_for(
                "message", timeout=self.client.timeout, check=check
            )
        except _base.TimeoutError:
            pass
        else:
            raise UnexpectedResponseError

    async def ask_human(self, query):
        """ Asks a human for an opinion on a question. Currently, only yes-no questions
            are supported. If the human answers 'no', the test will be failed.
        """
        message = await self.channel.send(query)
        await message.add_reaction("\u2714")
        await message.add_reaction("\u274C")

        def check(human_reaction, user):
            if human_reaction.count > 1:
                return human_reaction.message

        try:
            reaction: discord.Reaction = await self.client.wait_for(
                "reaction_add", timeout=self.client.timeout, check=check
            )
        except _base.TimeoutError:
            raise HumanResponseTimeout
        else:
            reaction, _ = reaction
            if reaction.emoji == "\u274c":
                raise HumanResponseFailure
