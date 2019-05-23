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
    sent = None
    if message.content == "ping?":
        sent = await message.channel.send("pong!")
    if message.content.startswith("Say something matching the regex"):
        sent = await message.channel.send("61")
    if message.content == "Please say 'epic!'":
        sent = await message.channel.send("epic!")
    if message.content.startswith("Say something containing 'gamer'"):
        sent = await message.channel.send("gamers r00l")
    if message.content.startswith("Post something with an image!"):
        sent = await message.channel.send("https://imgs.xkcd.com/comics/ui_vs_ux.png")
    if message.content.startswith("React with"):
        sent = await message.add_reaction("\u2714")

    if sent:
        print("Message sent: {}".format(sent.clean_content))


client.run(sys.argv[1])
