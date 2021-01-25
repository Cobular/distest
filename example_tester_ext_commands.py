"""
A case specifically setup to test that the patch in example_target_ext_commands.py works as intended.

    Run with:
        python example_tests.py TARGET_NAME TESTER_TOKEN
"""
import asyncio
import sys
from distest import TestCollector
from distest import run_dtest_bot

# The tests themselves

test_collector = TestCollector()
created_channel = None


@test_collector()
async def test_command(interface):
    await interface.assert_reply_contains("$test", "pong!")


# Actually run the bot

if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)
