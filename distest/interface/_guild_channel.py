from discord.abc import GuildChannel
from discord import TextChannel
from distest.exceptions import ResponseDidNotMatchError


async def assert_guild_channel_created(self, channel_name, timeout=None):
    """ Assert that the next channel created matches the name given

    :param str channel_name: The name of the channel to check for
    :param float timeout: The num of seconds to wait, defaults to the timeout provided at the start
    :returns: The channel that was created
    :rtype: discord.abc.GuildChannel
    :raises: NoResponseError
    """

    def check_for_channel_name(channel):
        return channel.name == channel_name

    return await self.wait_for_event(
        "guild_channel_create", check=check_for_channel_name, timeout=timeout
    )


async def assert_guild_channel_deleted(self, channel_name, timeout=None):
    """ Assert that the next channel deleted matches the name given

    TODO: check what the deleted channel actually returns

    :param str channel_name: The name of the channel to check for
    :param float timeout: The num of seconds to wait, defaults to the timeout provided at the start
    :returns: The channel that was deleted
    :rtype: discord.abc.GuildChannel
    :raises: NoResponseError
    """

    def check_for_channel_name(channel):
        return channel.name == channel_name

    return await self.wait_for_event(
        "guild_channel_delete", check=check_for_channel_name, timeout=timeout
    )


#
#
# async def assert_guild_channel_pin_content_equals(self, channel, message):
#     """ Checks when a channel has a message pinned, and that it matches the message provided. Doesn't work that well currently, maybe don't use
#
#     Useful to check if a specific message has been pinned.
#
#     For various reasons, this cannot currently check if the message was pinned or unpinned,
#         so please be careful to avoid any issues with mis-triggers. This may change in the future.
#
#     :param discord.TextChannel channel: The text channel to watch for pin changes on.
#     :param discord.Message message: The message to check the most recent pin against, compares IDs
#     """
#
#     # TODO: Check if I would use pins[0] or pins[-1] to get the most recent item
#
#     async def check(updated_channel, last_pin):
#         return updated_channel.id == channel.id
#
#     updated_channel, last_pin = await self.wait_for_event(
#         "guild_channel_pins_update", check=check, timeout=30
#     )
#
#     pins = await updated_channel.pins()
#
#     if pins[0].id == message.id:
#         return [updated_channel, last_pin]
#     else:
#         raise ResponseDidNotMatchError
#
#
# async def assert_guild_channel_unpin_content_equals(self, channel, message):
#     """ Checks when a channel's pin is updated.  Doesn't work at all rn, maybe don't use
#
#     """
#
#     def check(updated_channel,):
#         return updated_channel.id == channel.id
#
#     return
