# Distest

A small library used to write automated test for Discord bots.

Test framework originally written by [DXsmiley](https://github.com/DXsmiley), update to the rewrite and re-worked UI done by [me](https://github.com/JacobCover)

Just need to get command line stuff working reliably and this will be ready for a 0.1 pre-release. Until I get everything to a 1.0 though, expect the command line arguments and everything else to be volatile. In addition to the example here, my [main bot](https://github.com/JacobCover/ReplyBot) will be implementing this soon.

## Installation

Best way to get this running is to `git clone` it. The example bot's usage can be seen below.

## Usage

#### General
In order to use this package, you'll have to create *two* bot accounts. The first, referred to as the *target*, is the bot that you wish to test. If you're already here you probably have a token for this bot already. The second one, called the *tester* is responsible for running the tests.

The most important thing to know about this bot is that it has two modes, interactive and CLI. **Interactive mode** is used if you want to manually run the tests from inside discord. I also use it when testing the new tests. **CLI mode** allows you to start the bot and run the tests without any interaction, which is the mode that you will probably want to use when using this package in most cases. More information on how these two modes are used is available further down the readme.

First, you need to run the bot that you wish to test. You can run the example bot supplied with this repo as follows:
```
python example_bot.py TARGET_TOKEN
```

Then, you have to run the tester bot (This will run it in interactive mode - CLI mode demo shown later):
```
python example_tester.py TARGET_USERNAME TESTER_TOKEN
```

Make sure to use the username of the bot **without** the discriminator (#1111) or the bot won't understand what the user is

Once both bots are running, go to any discord channel that both bots have access to and type `::run all` to run all the tests. Use `::help` to get more information on the commands that the tester can use in interactive mode.

#### Making your own tester Bot
Start by writing functions to do the tests, examples can be seen in the example tester. Decorate the functions you want to be run as tests with `@distest.TestCollector()` and they will be available to be run. Instead of calling `run_bot()` like you would normally do to start a bot with discord.py, use `distest.run_dtest_bot()` and feed in the requested parameters. Based on the sysargs that are used to run the bot file, it will automatically run the bot in interactive or CLI mode. Basically, if you feed the bot the `-c` parameter to specify the channel that the tests should be run in, the bot will run those automatically. Otherwise, it will wait for the commands in discord as described below. 

### CLI Mode
CLI mode is designed to be used to run the tests in a normal way, such as on git hooks or a CI/CD pipeline. The following text is the usage snippet from the help command followed by some more general information from me. It isn't the same as the help message, as I tried to make it more in-depth. 

    usage: example_tester.py [-h] [-c channel]
                         [--run {all,test_reply_matches} | --stats]
                         target_bot_user tester_bot_token
                         

**Always Required**

- `target_bot_user`: The username (no discriminator) of the target bot. Same as described above in the general section.

- `tester_bot_token`: The token that will be used to run the tester bot. Also the same as described above in general.

**CLI Mode**

- `run`: Specifies if you will run all tests or a subset of them

- `stats`: Runs the bot in stats mode. Mutually exclusive with `run`. (Not very useful, may be removed. If you use it in some way, open an issue and let me know!)

- `channel`: The channel ID that the tests will be conducted in. Just need the int ID

**Other**

- `-h`: Just shows the help command. This is only the usage message, there is other information in the help.

**Sample Command**

The command I used to test this bot is available in run_tester.sh


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


## Contributing
Not much of note here, just that I use Black for formatting consistency, so please use that if you are contributing. If you don't, I will apply it during the PR but please just do that yourself. 

If you are adding new test types, please make sure you test them well to make sure they work as intended, and please add a demo of them in use to the `example_tests()` for others to see. And when you are done, please open a PR and I'll add it in!


## TODO
- [x] Update the Bot to the newly re-written discord.py 1.0
- [ ] Verify each test and add to `example_tests.py`
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
- [x] Allow running tests from the command line
    - [x] Add CLI mode section to the readme
    - [x] Have the bot return exit codes depending on test status
- [ ] More test types
- [ ] Prep for pip, get it packaged