# Dismock

A small library used to write automated test for Discord bots.

Currently in version `0.0.0`, since I'm still getting things set up in here.

## Installation

The project is not yet on PyPi, so you'll have to install from github.

```
pip install git+https://github.com/DXsmiley/dismock.git
```

## Usage

Command line arguments.

```
Usage:
	python -m dismock target_name token test_cases_module

target_name       - The username of the bot which you want to test
token             - The token used to run the dismock bot
test_cases_module - Filename of a python module containing some tests collected with a TestCollector
```

Example test file.

```
import dismock

testcollector = dismock.TestCollector()

async def test_ping(interface):
	await interface.assert_reply_equals('ping?', 'pong!')
```
