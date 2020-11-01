# Distest

[![CodeFactor](https://www.codefactor.io/repository/github/jakecover/distest/badge/?style=flat-square)](https://www.codefactor.io/repository/github/jakecover/distest/overview/?style=flat-square)
[![Build Status](https://img.shields.io/travis/JakeCover/distest/develop.svg?style=flat-square)](https://travis-ci.org/JakeCover/distest)
[![PyPi Version](https://img.shields.io/pypi/v/distest.svg?style=flat-square)](https://pypi.org/project/distest)
[![Discord Server](https://img.shields.io/discord/523301176309972993.svg?label=Discord)](https://discord.gg/Dah7RHH)


A small library used to write automated test for Discord bots.

Test framework originally written by [DXsmiley](https://github.com/DXsmiley), update to the rewrite and re-worked UI done by [me](https://github.com/JakeCover), with tons of help from [ALobsterDog](https://github.com/ALobsterDog)

Want to see the bots in action? Join us here on [discord](https://discord.gg/Dah7RHH) for help and to see the example bots whenever they are being tested. See you there!

One quick aside about changes and stuff for this project - I am now a full time student, which means that my open time has shot to nearly 0. I still want to keep this working going forwards, because I think it's a very powerful tool, but I want to let everyone know beforehand that my availability for helping out with things will be rather low. Knowing that, if you still want to use this, please do! I will try to fix major issues as soon as they are reported and I have time, but if you make a PR it will be a lot easier on me. Either way, thank you so much for considering using this tool on your project!

Command line stuff works now! We are at 0.2.0, but we will be at 1.0.0 in the not-so-far future once I check more items off the todo list below. Feel free to contribute, more hands is more better! Until we get there though, expect the command line arguments and everything else to be volatile. In addition to the example here, my [main bot](https://github.com/JacobCover/ReplyBot) will be implementing this soon(tm). (this has gone private for reasons, will be back in July-August)

## Installation

To use Distest with **your** bot, just install it:

`pip install distest`

This only includes the code to make your own tester, which is how this is meant to be used anyway. See `example_tester.py` for an example tester bot, and my other bto linked above soon(tm) for another more in depth example. 

## Usage

#### General
In order to use this package, you'll have to create *two* bot accounts. The first, referred to as the *target*, is the bot that you wish to test. If you're already here you probably have a token for this bot already. The second one, called the *tester* is responsible for running the tests.

The most important thing to know about the tester bot is that it has two modes, interactive and CLI. **Interactive mode** is used if you want to manually run the tests from inside discord. I use it when testing the new tests, better for development. **CLI mode** allows you to start the bot and run the tests without any interaction, which is the mode that you will probably want to use when using this package in most cases, like for CI/CD. More information on how these two modes are used is available further down the readme.

#### Making your own tester Bot
Start by writing functions to do the tests, examples can be seen in the example tester. Decorate the functions you want to be run as tests with `@distest.TestCollector()` and they will be available to be run. Instead of calling `run_bot()` like you would normally do to start a bot with discord.py, use `distest.run_dtest_bot()` and feed in the requested parameters. Based on the sysargs that are used to run the bot file, it will automatically run the bot in interactive or CLI mode. Basically, if you feed the bot the `-c` parameter to specify the channel that the tests should be run in, the bot will run those automatically. Otherwise, it will wait for the commands in discord as described below. 

### CLI Mode
CLI mode is designed to be used to run the tests in a normal way, such as on git hooks or a CI/CD pipeline. The following text is the usage snippet from the help command followed by some more general information from me. It isn't the same as the help message, as I tried to make it more in-depth. 

    usage: example_tester.py [-h] [-c channel]
                         [--run {all,test_reply_matches} | --stats]
                         target_bot_id tester_bot_token
                         

**Always Required**

- `target_bot_id`: The ID of the target bot. Same as described above in the general section.

- `tester_bot_token`: The token that will be used to run the tester bot. Also the same as described above in general.

**CLI Mode**

- `run`: Specifies if you will run all tests or a subset of them

- `stats`: Runs the bot in stats mode. Mutually exclusive with `run`. (Not very useful, may be removed. If you use it in some way, open an issue and let me know!)

- `channel`: The channel ID that the tests will be conducted in. Just need the int ID

**Other**

- `-h`: Just shows the help command. This is only the usage message, there is other information in the help.

**Sample Command**

The command I used to test this bot is available in run_tester.sh, Travis CI runs it to test the library.


### Interactive Mode Commands
Commands you can run in discord once the bot is running in interactive mode.

    ::stats
        Gives details about which tests have been
        run and what the results were

    ::run test_name
        Run a particular test. Options are methods decorated 
        with `@distest.TestCollector()` in the tester bot.

    ::run all
        Run all tests

    ::run unrun
        Run all tests that have not yet been run

    ::run failed
        Run all tests that failed on the most recent run

#### Interactive Mode Example:

First, you need to run the bot that you wish to test. You can run the example bot supplied with this repo as follows:
```
python example_target.py TARGET_TOKEN
```

Then, you have to run the tester bot (This will run it in interactive mode - CLI mode demo shown later):
```
python example_tester.py TARGET_ID TESTER_TOKEN
```

Once both bots are running, go to any discord channel that both bots have access to and type `::run all` to run all the tests. Use `::help` to get more information on the commands that the tester can use in interactive mode.


## Contributing
(see https://distest.readthedocs.io/en/latest/distest/getting-started-documentation.html for more up to date information)

Please open an issue for your contribution and tag it with contribution to discuss it. I recommend waiting for a response before pouring hours and hours into the contribution, but it will likely be approved either way. The other thing is to make sure you check the github project to see if there is someone else already working on it who you can help. Other notes:

* You may need to install the additional requirements from `requirements-dev.txt`. This is as simple as running `pip install -r requirements-dev.txt`. This larger list mostly includes things like black for formatting and sphinx for doc testing. 

* If you are adding new test types, please make sure you test them well to make sure they work as intended, and please add a demo of them in use to the `example_tests()` for others to see. When you are done, please open a PR and I'll add it in!

* I use Black for my code formatting, it would be appreciated if you could use it when contributing as well. I will remind you when you make a PR if you don't, it is essential to make sure that diffs aren't cluttered up with silly formatting changes. Additionally, CodeFactor *should* be tracking code quality and doing something with PRs. We will see soon exactly how that will work out.

* To build the docs for testing purposes, cd into the docs folder and run `make testhtml`. This will build to a set of HTML files you can view locally. 

* Make sure your issue goes onto the project, that's how we keep track of to-do and in progress things.

* Also, if you just want to propose an idea, create an issue and tag it with enhancement. The library is missing tons of features, so let me know what you want to see. Thank you for your help!