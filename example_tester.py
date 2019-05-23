"""
A functional demo of all possible test cases. This is the format you will want to use with your testing bot.

    Run with:
        python example_tests.py TARGET_NAME TESTER_TOKEN
"""

import sys
from distest import TestCollector
from distest import run_interactive_bot, run_dtest_bot

# The tests themselves

test_collector = TestCollector()


@test_collector()
async def test_ping(interface):
    await interface.assert_reply_contains("ping?", "pong!")


# @test_collector()
# async def test_reaction(interface):
#     await interface.ask_human("Click check")


@test_collector()
async def test_silence(interface):
    await interface.send_message("Shhhhh...")
    await interface.ensure_silence()


@test_collector()
async def test_reaction(interface):
    await interface.assert_reaction_equals("React with \u2714 please!", u"\u2714")


@test_collector()
async def test_reply_equals(interface):
    await interface.assert_reply_equals("Please say 'epic!'", "epic!")


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
async def test_reply_has_image(interface):
    await interface.assert_reply_has_image("Post something with an image!")


# Actually run the bot

if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)
