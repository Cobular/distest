# Dismock

A small library used to write automated test for Discord bots.

Currently in version `0.0.0`, since I'm still getting things set up in here.

## Installation

Best way to get this running is to `git clone` it.

## Usage

In order to use this package, you'll have to create *two* bot accounts. The first, referred to as the *target*, is the bot that you wish to test. If you're already here you probably have a token for this bot already. The second one, called the *tester* is responsible for running the tests.

First, you need to run the bot that you wish to test. You can run the example bot supplied with this repo as follows:
```
python example_bot.py TARGET_TOKEN
```

Then, you have to run the tester bot:
```
python example_tester.py TARGET_USERNAME TESTER_TOKEN
```

Once both bots are running, go to any discord channel that both bots have access to and type `::run all` to run all the tests. Use `::help` to get more information on the commands that the tester bot takes.
