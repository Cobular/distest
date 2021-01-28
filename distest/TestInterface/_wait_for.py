from distest.exceptions import NoResponseError
from typing import Callable, Optional
try:
    from asyncio.exceptions import TimeoutError
except (ImportError, ModuleNotFoundError):
    from concurrent.futures._base import TimeoutError


async def wait_for_reaction(self, message):
    """ Assert that ``message`` is reacted to with any reaction.

    :param discord.Message message: The message to test with
    :returns: The reaction object.
    :rtype: discord.Reaction
    :raises NoReactionError:
    """

    def check_reaction(reaction, user):
        return (
            reaction.message.id == message.id
            and user == self.target
            and reaction.message.channel == self.channel
        )

    try:
        result = await self.client.wait_for(
            "reaction_add", timeout=self.client.timeout, check=check_reaction
        )
    except TimeoutError:
        raise NoResponseError
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
            "message", timeout=self.client.timeout, check=self._check_message
        )
    except TimeoutError:
        raise NoResponseError
    else:
        return result


async def wait_for_message_in_channel(self, content, channel_id):
    """ Send a message with ``content`` and returns the next message that the targeted bot sends. Used in many other
    tests.

    :param str content: The text of the trigger message.
    :param int channel_id: The id of the channel that the message is sent in.
    :returns: The message we've been waiting for.
    :rtype: discord.Message
    :raises: NoResponseError
    """

    def check_for_message_in_channel(message):
        return message.channel.id == channel_id and message.content == content

    return await self.wait_for_event(
        "message", check=check_for_message_in_channel, timeout=30
    )


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


async def wait_for_event(
    self, event: str, check: Optional[Callable[..., bool]] = None, timeout: float = None
):
    """ A wrapper for the discord.py function :py:func:`wait_for <discord.Client.wait_for>`, tuned to be useful for distest.

    See https://discordpy.readthedocs.io/en/latest/api.html#event-reference for a list of events.

    :param event: The discord.py event, as a string and with the ``on_`` removed from the beginning.
    :param Callable[...,bool] check: A check function that all events of the type are ran against. Should return true when the desired event occurs, takes the event's params as it's params
    :param float timeout: How many seconds to wait for the event to occur.
    :return: The parameters of the event requested
    :raises: NoResponseError
    """
    if timeout is None:
        timeout = self.client.timeout

    try:
        result = await self.client.wait_for(event, timeout=timeout, check=check)
    except TimeoutError:
        raise NoResponseError
    # TODO: What happens if the event is wrong / not valid?
    else:
        return result
