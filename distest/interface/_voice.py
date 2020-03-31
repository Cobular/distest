async def connect(self, channel):
    """
    Connect to a given VoiceChannel
    :param channel: The VoiceChannel to connect to.
    :return:
    """
    self.voice_channel = self.client.get_channel(channel)
    self.voice_client = await self.voice_channel.connect()


async def disconnect(self):
    """
    Disconnect from the VoiceChannel; Doesn't work if the Bot isn't connected.
    :return:
    """
    if self.voice_channel is None:
        raise NotImplementedError("The Bot isn't connected.")
    await self.voice_client.disconnect()
