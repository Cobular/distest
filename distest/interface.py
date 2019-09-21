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
    """ Holds data about a specific test.

    :param str name: The name of the test, checks this against the valid test names
    :param function func: The function in the tester bot that makes up this test
    :param bool needs_human: Weather or not this test will require human interaction to complete
    :raises: ValueError
    """

    def __init__(self, name, func, needs_human=False):
        if name in SPECIAL_TEST_NAMES:
            raise ValueError("{} is not a valid test name".format(name))
        self.name = name
        self.func = func
        self.last_run = 0
        self.result = TestResult.UNRUN
        self.needs_human = needs_human


class TestInterface:
    """ All the tests, and some supporting functions. Tests are designed to be run
    by the tester and mixed together in order to actually test the bot.

    .. note::
        In addition to the tests failing due to their own reasons, all tests will also fail if they timeout.
        This period is specified when the bot is run.

    .. note::
        Some functions (``send_message`` and ``edit_message``) are helper functions rather than tests and serve to bring
        some of the functionality of the discord library onto the same level as the tests.

    .. note::
        ``assert_reply_*`` tests will send a message with the passed content, while ``assert_message_*`` tests require a
        ``Message`` to be passed to them. This allows for more flexibility when you need it and an easier
        option when you don't.

    :param discord.Client client: The discord client of the tester.
    :param discord.TextChannel channel: The discord channel in which to run the tests.
    :param discord.Member target: The bot we're testing.
    """

    def __init__(self, client, channel, target):
        self.client = client
        self.channel = channel
        self.target = target
        self.voice_client = None
        self.voice_channel = None

    async def send_message(self, content):
        """ Send a message to the channel the test is being run in. **Helper Function**

        :param str content: Text to send in the message
        :returns: The message that was sent
        :rtype: discord.Message
        """
        return await self.channel.send(content)

    def _checkMessage(self, message):
        return message.channel == self.channel and message.author == self.target

    async def connect(self, channel):
        """
        Connect to a given VoiceChannel
        :param channel: The VoiceChannel to connect to.
        :return:
        """
        self.voice_channel: discord.VoiceChannel = self.client.get_channel(channel)
        self.voice_client: discord.VoiceClient = await self.voice_channel.connect()

    async def disconnect(self):
        """
        Disconnect from the VoiceChannel; Doesn't work if the Bot isn't connected.
        :return:
        """
        if self.voice_channel is None:
            raise NotImplementedError("The Bot isn't connected.")
        await self.voice_client.disconnect()

    @staticmethod
    async def edit_message(message, new_content):
        """ Modify a message. Most tests and ``send_message`` return the ``discord.Message`` they sent, which can be
        used here. **Helper Function**

        :param discord.Message message: The target message. Must be a ``discord.Message``
        :param str new_content: The text to change `message` to.
        :returns: `message` after modification.
        :rtype: discord.Message
        """
        return await message.edit(content=new_content)

    async def wait_for_reaction(self, message):
        """ Assert that ``message`` is reacted to with any reaction.

        :param discord.Message message: The message to test with
        :returns: The reaction object.
        :rtype: discord.Reaction
        :raises NoReactionError:
        """

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
        """ Wait for the bot the send any message. Will fail on timeout, but will ignore messages sent by anything other
        that the target.

        :returns: The message we've been waiting for.
        :rtype: discord.Message
        :raises: NoResponseError
        """
        try:
            result = await self.client.wait_for(
                "message", timeout=self.client.timeout, check=self._checkMessage
            )
        except _base.TimeoutError:
            raise NoResponseError
        else:
            return result

    async def wait_for_reply(self, content):
        """ Send a message with ``content`` and returns the next message that the targeted bot sends. Used in many other
        tests.

        :param str content: The text of the trigger message.
        :returns: The message we've been waiting for.
        :rtype: discord.Message
        :raises: NoResponseError
        """
        await self.channel.send(content)
        return await self.wait_for_message()

    async def get_delayed_reply(
        self, seconds_to_wait, assert_function, argument_list=[]
    ):
        """
        Get the last reply after a specific time and assert it to a test.
        :param seconds_to_wait: Time to wait in s
        :param assert_function: The function to call afterwards, without parenthesis
            (assert_message_equals, not assert_message_equals()!)
        :param argument_list: The arguments to pass, required is the first one,
            which is the expected result to compare to.
        :rtype argument_list: list
        :return:
        """
        if argument_list is None:
            argument_list = []
        await asyncio.sleep(seconds_to_wait)
        message: discord.Message = self.channel.last_message
        if len(argument_list) == 1:
            return await assert_function(message, argument_list[0])
        elif len(argument_list) == 2:
            return await assert_function(
                message, argument_list[0], attributes_to_prove=argument_list[1]
            )
        else:
            raise SyntaxError("Invalid Number of Arguments")

    async def assert_embed_equals(
        self,
        message: discord.Message,
        matches: discord.Embed,
        attributes_to_prove: list = None,
    ):
        """
        If ``matches`` doesn't match the embed of ``message``, fail the test.
        :param message: original message
        :param matches: embed object to compare to
        :param attributes_to_prove: a string list with the attributes of the embed, which are to compare
        This are all the Attributes you can prove: "title", "description", "url", "color", "author", "video",
        "image" and "thumbnail".
        :return: message
        :rtype: discord.Message
        """

        # All possible attributes a user can set during initialisation
        possible_attributes = [
            "title",
            "description",
            "url",
            "color",
            "author",  # This is not the original author of the message, author is a attribute you are able to set.
            "video",
            "image",
            "thumbnail",
        ]
        # View all (visible) attributes visualized here: https://imgur.com/a/tD7Ibc4

        attributes = []

        # Proves, if the attribute provided by the user is a valid attribute to check
        if attributes_to_prove is not None:
            for value in attributes_to_prove:
                if value not in possible_attributes:
                    raise NotImplementedError(
                        '"' + value + '" is not a possible value.'
                    )
                attributes.append(value)
        else:
            # If no attributes to check are provided, check them all.
            attributes = possible_attributes

        for embed in message.embeds:
            for attribute in attributes:
                if attribute == "image" or attribute == "thumbnail":
                    # Comparison of Embedded Images / Thumbnails
                    if getattr(getattr(embed, attribute), "url") != getattr(
                        getattr(matches, attribute), "url"
                    ):
                        raise ResponseDidNotMatchError(
                            "The {} attribute did't match".format(attribute)
                        )
                elif attribute == "video":
                    # Comparison of Embedded Video
                    if getattr(getattr(embed, "video"), "url") != getattr(
                        getattr(matches, "video"), "url"
                    ):
                        raise ResponseDidNotMatchError(
                            "The video attribute did't match"
                        )
                elif attribute == "author":
                    # Comparison of Author
                    if getattr(getattr(embed, "author"), "name") != getattr(
                        getattr(matches, "author"), "name"
                    ):
                        raise ResponseDidNotMatchError(
                            "The author attribute did't match"
                        )
                elif not getattr(embed, attribute) == getattr(matches, attribute):
                    print(
                        "Did not match:",
                        attribute,
                        getattr(embed, attribute),
                        getattr(matches, attribute),
                    )
                    raise ResponseDidNotMatchError
        return message

    async def assert_message_equals(self, message, matches):
        """ If ``message`` does not match a string exactly, fail the test.

        :param discord.Message message: The message to test.
        :param str matches: The string to test `message` against.
        :returns: `message`
        :rtype: discord.Message
        :raises: ResponseDidNotMatchError
        """
        if message.content != matches:
            raise ResponseDidNotMatchError
        return message

    async def assert_message_contains(self, message, substring):
        """ If `message` does not contain the given substring, fail the test.

        :param discord.Message message: The message to test.
        :param str substring: The string to test `message` against.
        :returns: `message`
        :rtype: discord.Message
        :raises: ResponseDidNotMatchError
        """
        if substring not in message.content:
            raise ResponseDidNotMatchError
        return message

    async def assert_message_matches(self, message, regex):
        """ If `message` does not match a regex, fail the test.

        Requires a properly formatted Python regex ready to be used in the ``re`` functions.


        :param discord.Message message: The message to test.
        :param str regex: The regular expression to test `messsage` against.
        :returns: `message`
        :rtype: discord.Message
        :raises: ResponseDidNotMatchError
        """
        if not re.match(regex, message.content):
            raise ResponseDidNotMatchError
        return message

    async def assert_message_has_image(self, message):
        """ Assert `message` has an attachment. If not, fail the test.

        :param discord.Message message: The message to test.
        :returns: `message`
        :rtype: discord.Message
        :raises: UnexpectedResponseError
        """
        if message.attachments == [] and message.embeds == []:
            raise UnexpectedResponseError
        return message

    async def assert_reply_equals(self, contents, matches):
        """ Send a message and wait for a response. If the response does not match the string
        exactly, fail the test.

        :param str contents: The content of the trigger message. (A command)
        :param str matches: The string to test against.
        :returns: The reply.
        :rtype: discord.Message
        :raises: ResponseDidNotMatchError
        """
        response = await self.wait_for_reply(contents)
        return await self.assert_message_equals(response, matches)

    async def assert_reply_contains(self, contents, substring):
        """ Send a message and wait for a response. If the response does not contain
        the given substring, fail the test.

        :param str contents: The content of the trigger message. (A command)
        :param str substring: The string to test against.
        :returns: The reply.
        :rtype: discord.Message
        :raises: ResponseDidNotMatchError
        """
        response = await self.wait_for_reply(contents)
        return await self.assert_message_contains(response, substring)

    async def assert_reply_matches(self, contents, regex):
        """ Send a message and wait for a response. If the response does not match a regex, fail the test.

        Requires a properly formatted Python regex ready to be used in the ``re`` functions.

        :param str contents: The content of the trigger message. (A command)
        :param str regex: The regular expression to test against.
        :returns: The reply.
        :rtype: discord.Message
        :raises: ResponseDidNotMatchError
        """
        response = await self.wait_for_reply(contents)
        return await self.assert_message_matches(response, regex)

    async def assert_reaction_equals(self, contents, emoji):
        """ Send a message and ensure that the reaction is equal to `emoji`. If not, fail the test.

        :param str contents: The content of the trigger message. (A command)
        :param discord.Emoji emoji: The emoji that the reaction must equal.
        :returns: The resultant reaction object.
        :rtype: discord.Reaction
        :raises: ReactionDidNotMatchError
        """
        reaction = await self.wait_for_reaction(await self.send_message(contents))
        if str(reaction[0].emoji) != emoji:
            raise ReactionDidNotMatchError
        return reaction

    async def assert_reply_has_image(self, contents):
        """Send a message consisting of `contents` and wait for a reply.

        Check that the reply contains a ``discord.Attachment``. If not, fail the test.

        :param str contents: The content of the trigger message. (A command)
        :returns: The reply.
        :rtype: discord.Message
        :raises: ResponseDidNotMatchError, NoResponseError
        """
        message = await self.wait_for_reply(contents)
        await asyncio.sleep(1)  # Give discord a moment to add the embed if its a link
        return await self.assert_message_has_image(message)

    async def ensure_silence(self):
        """ Assert that the bot does not post any messages for some number of seconds.

        :raises: UnexpectedResponseError, TimeoutError
        """
        try:
            await self.client.wait_for(
                "message", timeout=self.client.timeout, check=self._checkMessage
            )
        except _base.TimeoutError:
            pass
        else:
            raise UnexpectedResponseError

    async def ask_human(self, query):
        """ Ask a human for an opinion on a question using reactions.

        Currently, only yes-no questions are supported. If the human answers 'no', the test will be failed. Do not use
        if avoidable, since this test is not really automateable. Will fail if the reaction is wrong or takes too long
        to arrive

        :param str query: The question for the human.
        :raises: HumanResponseTimeout, HumanResponseFailure
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
