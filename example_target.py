"""
This bot is a sample bot that is used to demonstrate the testing functionality.

It does not run the tests, just exists to have tests run on it.

    Run with:
        python example_target.py TARGET_TOKEN
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
