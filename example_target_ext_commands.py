from discord.ext import commands
import sys

bot = commands.Bot(command_prefix='$')

# Below is an example of how to patch your bot for testing
if sys.argv[2] == "TESTING":
    from distest.patches import patch_target
    bot = patch_target(bot)


@bot.event
async def on_ready():
    print("Bot is awake and ready!")


@bot.command()
async def test(ctx):
    await ctx.send("pong!")

#
# @bot.event
# async def on_message(message):
#     await bot.process_commands(message)


bot.run(sys.argv[1])
