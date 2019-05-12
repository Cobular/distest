"""
    Run with:
        python example_bot.py TARGET_TOKEN
"""

import sys

import discord

client = discord.Client()


@client.event
async def on_ready():
    print("Ready")


@client.event
async def on_message(message):
    if message.content == "ping?":
        print("Replying")
        await message.channel.send("pong!")


client.run(sys.argv[1])
