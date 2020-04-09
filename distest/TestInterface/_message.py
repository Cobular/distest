from distest.exceptions import ResponseDidNotMatchError, UnexpectedResponseError
from re import match


async def assert_message_equals(message, matches):
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


async def assert_message_contains(message, substring):
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


async def assert_message_matches(message, regex):
    """ If `message` does not match a regex, fail the test.

    Requires a properly formatted Python regex ready to be used in the ``re`` functions.


    :param discord.Message message: The message to test.
    :param str regex: The regular expression to test `message` against.
    :returns: `message`
    :rtype: discord.Message
    :raises: ResponseDidNotMatchError
    """
    if not match(regex, message.content):
        raise ResponseDidNotMatchError
    return message


async def assert_message_has_image(message):
    """ Assert `message` has an attachment. If not, fail the test.

    :param discord.Message message: The message to test.
    :returns: `message`
    :rtype: discord.Message
    :raises: UnexpectedResponseError
    """
    if message.attachments == [] and message.embeds == []:
        raise UnexpectedResponseError
    return message
