"""
    Run with:
        python example_tests.py TARGET_NAME TESTER_TOKEN
    Exists as a functional demo of all possible test cases
"""

import sys
from dismok import TestCollector
from dismok import run_interactive_bot
# The tests themselves

test_collector = TestCollector()


# @test_collector()
# async def test_ping(interface):
#     await interface.assert_message_contains('ping?')


# @test_collector()
# async def test_reaction(interface):
#     await interface.ask_human("Click check")


# @test_collector()
# async def test_silence(interface):
#     await interface.ensure_silence("Shhhhh...")


# @test_collector()
# async def test_reaction(interface):
#     await interface.assert_reaction_equals("React with \u2714 please!", u'\u2714')


# @test_collector()
# async def test_reply_equals(interface):
#     await interface.assert_reply_equals("Please say 'epic!'", "epic!")


# @test_collector()
# async def test_reply_contains(interface):
#     await interface.assert_reply_contains("Say something containing 'gamer' please!", "gamer")


@test_collector()
async def test_reply_matches(interface):
    await interface.assert_reply_matches("Say something matching the regex `[0-9]{1,3}`", r"[0-9]{1,3}")


# Make it easy to run the tests

if __name__ == '__main__':
    _, target_name, token = sys.argv
    run_interactive_bot(target_name, token, test_collector)
