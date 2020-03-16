"""
A functional demo of all possible test cases. This is the format you will want to use with your testing bot.

    Run with:
        python example_tests.py TARGET_NAME TESTER_TOKEN
"""
import asyncio
import sys
from distest import TestCollector
from distest import run_interactive_bot, run_dtest_bot

# The tests themselves

test_collector = TestCollector()


@test_collector()
async def test_ping(interface):
    await interface.assert_reply_contains("ping?", "pong!")


@test_collector()
async def test_delayed_reply(interface):
    message = await interface.send_message("Say some stuff, but at 4 seconds, say 'yeet'")
    await interface.get_delayed_reply(5, interface.assert_message_equals, "yeet")


@test_collector()
async def test_reaction(interface):
    await interface.assert_reaction_equals("React with \u2714 please!", u"\u2714")


@test_collector()
async def test_reply_equals(interface):
    await interface.assert_reply_equals("Please say 'epic!'", "epic!")


@test_collector()
async def test_silence(interface):
    await interface.send_message("Shhhhh...")
    await interface.ensure_silence()


@test_collector()
async def test_reply_contains(interface):
    await interface.assert_reply_contains(
        "Say something containing 'gamer' please!", "gamer"
    )


@test_collector()
async def test_reply_matches(interface):
    await interface.assert_reply_matches(
        "Say something matching the regex `[0-9]{1,3}`", r"[0-9]{1,3}"
    )


@test_collector()
async def test_ask_human(interface):
    await interface.ask_human("Click the Check!")


@test_collector()
async def test_reply_has_image(interface):
    await interface.assert_reply_has_image("Post something with an image!")


@test_collector()
async def test_reply_on_edit(interface):
    message = await interface.send_message("Say 'Yeah, that cool!'")
    await asyncio.sleep(1)
    await interface.edit_message(message, "Say 'Yeah, that is cool!'")
    await interface.assert_message_contains(message, "Yeah, that is cool!")


# Actually run the bot

if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)
