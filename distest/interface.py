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
        self.name = name
        self.func = func
        self.last_run = 0
        self.result = TestResult.UNRUN
        self.needs_human = needs_human


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
        self.client = client
        self.channel = channel
        self.target = target

    async def send_message(self, content):
        """ Send a message to the testing channel.

        :rtype discord.Message:
        """
        return await self.channel.send(content)

    def checkMessage(self, message):
        return message.channel == self.channel and message.author == self.target

    @staticmethod
    async def edit_message(message: discord.Message, new_content):
        """ Modify a message."""
        return await message.edit(content=new_content)

    async def wait_for_reaction(self, message: discord.Message):
        """ Assert that ``message`` is reacted to."""

        def checkReaction(reaction, user):
            return (
                reaction.message.id == message.id
                and user == self.target
                and reaction.message.channel == self.channel
            )

        try:
            result = await self.client.wait_for(
                "reaction_add", timeout=self.client.timeout, check=checkReaction
            )
        except _base.TimeoutError:
            raise NoReactionError
        else:
            return result

    async def wait_for_message(self):
        """ Wait for the bot the send a message.
            If the bot takes longer than 5 seconds (default) the test fails.
        """
        try:
            result = await self.client.wait_for(
                "message", timeout=self.client.timeout, check=self.checkMessage
            )
        except _base.TimeoutError:
            raise NoResponseError
        else:
            return result

    async def wait_for_reply(self, content):
        """ Send a message and returns the next message that the targeted bot sends. """
        await self.channel.send(content)
        return await self.wait_for_message()

    async def assert_embed_equals(
        self, message: discord.Message, matches: discord.Embed
    ):
        """ If the first embed does not equal the given one, fail the test"""
        if message.embeds[0].title is not matches.title:
            # TODO: Until now only compares the titles, needs to be extended to all the attributes
            raise ResponseDidNotMatchError
        return message

    async def assert_message_equals(self, message: discord.Message, matches):
        """ If `message` does not match a string exactly, fail the test."""
        if message.content != matches:
            raise ResponseDidNotMatchError
        return message

    async def assert_message_contains(self, message: discord.Message, substring):
        """ If `message` does not contain the given substring, fail the test."""
        if substring not in message.content:
            raise ResponseDidNotMatchError
        return message

    async def assert_message_matches(self, message: discord.Message, regex):
        """ If `message` does not match a regex, fail the test."""
        if not re.match(regex, message.content):
            raise ResponseDidNotMatchError
        return message

    async def assert_message_has_image(self, message: discord.Message):
        """ Assert ``message`` has an attachment. If not, fail the test."""
        if message.attachments == [] and message.embeds == []:
            raise UnexpectedResponseError
        return message

    async def assert_reply_equals(self, contents: str, matches: str):
        """ Send a message and wait for a response.
            If the response does not match a string exactly, fail the test.
        """
        response = await self.wait_for_reply(contents)
        return await self.assert_message_equals(response, matches)

    async def assert_reply_contains(self, contents: str, substring: str):
        """ Send a message and wait for a response.
            If the response does not contain the given substring, fail the test.
        """
        response = await self.wait_for_reply(contents)
        return await self.assert_message_contains(response, substring)

    async def assert_reply_embed_equals(self, message: str, equals: discord.Embed):
        response = await self.wait_for_reply(message)
        return await self.assert_embed_equals(response, equals)

    async def assert_reply_matches(self, contents: str, regex):
        """ Send a message and wait for a response. If the response does not
            match a regex, fail the test. Requires a properly formatted Python regex
            ready to be used in the ``re`` functions.
        """
        response = await self.wait_for_reply(contents)
        return await self.assert_message_matches(response, regex)

    async def assert_reaction_equals(self, contents, emoji):
        """ Send a message and ensure that the reaction is equal to ``emoji``"""
        reaction = await self.wait_for_reaction(await self.send_message(contents))
        if str(reaction[0].emoji) != emoji:
            raise ReactionDidNotMatchError
        return reaction

    async def assert_reply_has_image(self, contents: str) -> discord.Message:
        """Send a message consisting of ``contents`` and wait for a reply.
           Check that the reply contains an attachment. If not, fail the test.
        """
        message = await self.wait_for_reply(contents)
        await asyncio.sleep(1)  # Give discord a moment to add the embed if its a link
        return await self.assert_message_has_image(message)

    async def ensure_silence(self):
        """ Assert that the bot does not post any messages for some number of seconds. """
        try:
            await self.client.wait_for(
                "message", timeout=self.client.timeout, check=self.checkMessage
            )
        except _base.TimeoutError:
            pass
        else:
            raise UnexpectedResponseError

    async def ask_human(self, query):
        """ Ask a human for an opinion on a question. Currently, only yes-no questions
            are supported. If the human answers 'no', the test will be failed.
        """
        message = await self.send_message(query)
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
