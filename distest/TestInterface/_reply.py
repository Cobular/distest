from asyncio import sleep
from inspect import signature, _ParameterKind
from typing import Dict

from discord import Embed, Message


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


async def assert_reply_embed_equals(
        self, message: str, equals: Embed, attributes_to_check: list = None
):
    """ Send a message and wait for an embed response. If the response does not match the given embed in the listed
    attributes, fail the test

    See examples in example_target.py for examples of use.

    :param message:
    :param equals: :py:class:`embed <discord.Embed>` object to compare to
    :param attributes_to_check: a string list with the attributes of the embed, which are to compare
        This are all the Attributes you can prove: "title", "description", "url", "color",
        "author", "video", "image" and "thumbnail".
    :return: message
    :rtype: discord.Message
    """
    response = await self.wait_for_reply(message)
    return await self.assert_embed_equals(
        response, equals, attributes_to_prove=attributes_to_check
    )


async def assert_reply_embed_regex(self, message: str, patterns: Dict[str, str]):
    """ Send a message and wait for a response. If the response is not an embed or does not match the regex,
        fail the test.

    See examples in example_target.py for examples of use.

    :param message:
    :param patterns: A dict of the attributes to check. See
        :py:meth:`assert_message_contains <distest.TestInterface.assert_embed_regex>` for more info on this.
    :return: message
    :rtype: discord.Message
    """
    response = await self.wait_for_reply(message)
    return await self.assert_embed_regex(response, patterns)


async def assert_reply_matches(self, contents: str, regex):
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


async def assert_reply_has_image(self, contents):
    """Send a message consisting of `contents` and wait for a reply.

    Check that the reply contains a ``discord.Attachment``. If not, fail the test.

    :param str contents: The content of the trigger message. (A command)
    :returns: The reply.
    :rtype: discord.Message
    :raises: ResponseDidNotMatchError, NoResponseError
    """
    message = await self.wait_for_reply(contents)
    await sleep(1)  # Give discord a moment to add the embed if its a link
    return await self.assert_message_has_image(message)


async def get_delayed_reply(self, seconds_to_wait, test_function, *args):
    """Get the last reply after a specific time and check it against a given test.

    :param float seconds_to_wait: Time to wait in s
    :param method test_function: The function to call afterwards, without parenthesis
        (assert_message_equals, not assert_message_equals()!)
    :param args: The arguments to pass to the test, requires the same number of args as the test function.
        Make sur to pass in **all** args, including kwargs with defaults.
        NOTE: this policy may change if it becomes kinda stupid down the road.
    :rtype: Method
    :raises SyntaxError:
    :returns: The instance of the test requested
    """

    def parse_parameters(method) -> list:
        kwarg, parg, either, var_kwarg, var_parg = 0, 0, 0, 0, 0
        for i in signature(method).parameters:
            j = signature(method).parameters[i]
            if j.kind == _ParameterKind.KEYWORD_ONLY:
                kwarg += 1
            if j.kind == _ParameterKind.POSITIONAL_ONLY:
                parg += 1
            if j.kind == _ParameterKind.POSITIONAL_OR_KEYWORD:
                either += 1
            if j.kind == _ParameterKind.VAR_KEYWORD:
                var_kwarg += 1
            if j.kind == _ParameterKind.VAR_POSITIONAL:
                var_parg += 1
        return [kwarg, parg, either, var_kwarg, var_parg]

    desired_method_parameters = parse_parameters(test_function)
    num_desired_parameters = sum(desired_method_parameters[0:3]) - 1
    if len(args) != num_desired_parameters:
        raise SyntaxError("Invalid Number of Arguments")

    await sleep(seconds_to_wait)
    message: Message = self.channel.last_message
    return await test_function(message, *args)
