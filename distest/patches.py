"""
Contains the code required to patch out the fact that :py:class:`Bot <discord.ext.commands.Bot>` class ignores messages
from other bots.

This should be used if you have a target bot that uses the :py:class:`ext.commands.Bot <discord.ext.commands.Bot>`
system, as otherwise it's commands will ignore messages from the tester bot.


"""
from discord.ext.commands.bot import Bot


async def process_commands(self, message):
    ctx = await self.get_context(message)
    await self.invoke(ctx)


def patch_target(bot):
    """
    Patches the target bot. It changes the ``process_commands`` function to remove the check if the received message
    author is a bot or not.

    :param discord.ext.commands.Bot bot:
    :return: The patched bot.
    """
    if type(bot) == Bot:
        bot.process_commands = process_commands.__get__(bot, Bot)
    return bot
