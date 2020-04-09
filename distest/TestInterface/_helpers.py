async def send_message(self, content):
    """ Send a message to the channel the test is being run in. **Helper Function**

    :param str content: Text to send in the message
    :returns: The message that was sent
    :rtype: discord.Message
    """
    return await self.channel.send(content)


def _check_message(self, message):
    return message.channel == self.channel and message.author == self.target


async def edit_message(message, new_content):
    """ Modify a message. Most tests and ``send_message`` return the ``discord.Message`` they sent, which can be
    used here. **Helper Function**

    :param discord.Message message: The target message. Must be a ``discord.Message``
    :param str new_content: The text to change `message` to.
    :returns: `message` after modification.
    :rtype: discord.Message
    """
    return await message.edit(content=new_content)
