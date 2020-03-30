"""
This bot is a sample bot that is used to demonstrate the testing functionality.

It does not run the tests, just exists to have tests run on it.

    Run with:
        python example_target.py TARGET_TOKEN
"""
import asyncio
import sys

import discord

client = discord.Client()


@client.event
async def on_ready():
    print("Ready")


@client.event
async def on_message(message):
    if message.author.id is client.user.id:
        return
    sent = None
    if message.content == "ping?":
        await asyncio.sleep(1)
        sent = await message.channel.send("pong!")
    if message.content.startswith("Say something matching the regex"):
        await asyncio.sleep(1)
        sent = await message.channel.send("61")
    if message.content == "Please say 'epic!'":
        await asyncio.sleep(1)
        sent = await message.channel.send("epic!")
    if message.content.startswith("Say something containing 'gamer'"):
        await asyncio.sleep(1)
        sent = await message.channel.send("gamers r00l")
    if message.content.startswith("Post something with an image!"):
        await asyncio.sleep(1)
        sent = await message.channel.send("https://imgs.xkcd.com/comics/ui_vs_ux.png")
    if message.content.startswith("React with"):
        await asyncio.sleep(1)
        sent = await message.add_reaction("\u2714")
    if message.content.startswith("Click the Check!"):
        await asyncio.sleep(1)
        sent = await message.add_reaction("\u2714")
    if message.content.startswith("Test the Embed!"):
        await asyncio.sleep(1)
        embed = discord.Embed(
            title="This is a test!",
            description="Descriptive",
            url="http://www.example.com",
            color=0x00FFCC,
        )
        embed.set_author(name="Author")
        embed.set_image(
            url="https://upload.wikimedia.org/wikipedia/commons/4/40/Test_Example_%28cropped%29.jpg"
        )
        embed.set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/4/40/Test_Example_%28cropped%29.jpg"
        )
        sent = await message.channel.send(embed=embed)
    if message.content.startswith("Test the Part Embed!"):
        await asyncio.sleep(1)
        embed = discord.Embed(title="Testing Title.", description="Right Description!")
        sent = await message.channel.send(embed=embed)
    if message.content.startswith("Say some stuff, but at 4 seconds, say 'yeet'"):
        await asyncio.sleep(1)
        await message.channel.send("hahaha!")
        await message.channel.send("No!")
        await message.channel.send("Ok...")
        await asyncio.sleep(2.5)
        sent = await message.channel.send("yeet")
    if message.content.startswith("Create a tc called yeet"):
        await asyncio.sleep(1)
        await message.guild.create_text_channel("yeet")
    if sent is not None:
        print("Message sent: {}".format(sent.clean_content))


@client.event
async def on_message_edit(before, after):
    sent = None
    if after.content.startswith("Say 'Yeah, that is cool!'"):
        await asyncio.sleep(1)
        sent = await after.channel.send("Yeah, that is cool!")
    if sent is not None:
        print("Message sent: {}".format(sent.clean_content))


client.run(sys.argv[1])
