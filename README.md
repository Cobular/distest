# Distest

A small library used to write automated test for Discord bots.

Bulk was written by [DXsmiley](https://github.com/DXsmiley), updated to the rewrite and modified a bit by [me](https://github.com/JacobCover)

Currently in pre-alpha, since I'm figuring out how this works. In addition to the example here, my [main bot](https://github.com/JacobCover/ReplyBot) will be implementing this soon.

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

Make sure to use the username of the bot **without** the discriminator (#1111) or the bot won't understand what the user is

Once both bots are running, go to any discord channel that both bots have access to and type `::run all` to run all the tests. Use `::help` to get more information on the commands that the tester bot takes.

## Options
Commands you can run in discord once the bot is up. 

    ::stats
        Gives details about which tests have been
        run and what the results were

    ::run test_name
        Run a particular test

    ::run all
        Run all tests

    ::run unrun
        Run all tests that have not yet been run

    ::run failed
        Run all tests that failed on the most recent run


## New Tests
I'm still figuring this part out, but it seems that you write tests in the testing bot and decorate them with an instance of `distest.TestCollector()`. Then, you can run the bot and use the run commands to run the tests.


## TODO
- [x] Update the Bot to the newly re-written discord.py 1.0
- [ ] Test each test
    - [ ] send_message
    - [ ] edit_message
    - [ ] wait_for_reaction
    - [ ] wait_for_message
    - [ ] wait_for_reply
    - [ ] assert_message_equals
    - [x] assert_message_contains
    - [ ] assert_message_matches
    - [x] assert_reply_equals
    - [x] assert_reply_contains
    - [x] assert_reply_matches
    - [x] assert_reaction_equals
    - [x] ensure_silence
    - [x] ask_human
- [ ] Allow running tests from the command line