async def assert_channel_created(self, channel_name, timeout=None):
    """ Assert that the next channel created matches the name given

    :param str channel_name: The name of the channel to check for
    :param float timeout: The num of seconds to wait, defaults to the timeout provided at the start
    :returns: The channel
    :rtype discord.abc.GuildChannel:
    :raises: NoResponseError
    """

    def check_for_channel_name(channel):
        return channel.name == channel_name

    return await self.wait_for_event("guild_channel_create", check=check_for_channel_name, timeout=30)