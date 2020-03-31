from distest.exceptions import NoResponseError
from concurrent.futures import _base



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
    except _base.TimeoutError:
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
