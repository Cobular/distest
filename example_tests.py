"""
    Run with:
        python example_tests.py TARGET_NAME TESTER_TOKEN
"""

import sys
import dismock

# The tests themselves

test_collector = dismock.TestCollector()


@test_collector()
async def test_ping(interface):
    await interface.assert_message_contains('ping?')


@test_collector()
async def test_reaction(interface):
    await interface.ask_human("Click check")
    print("Done")


# Make it easy to run the tests

if __name__ == '__main__':
    _, target_name, token = sys.argv
    dismock.run_interactive_bot(target_name, token, test_collector)
