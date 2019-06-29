.. _quickstart:

Quickstart
==========

Installation
------------

1. Install the library with pip:
     ``pip install distest``
2. Distest works by using a second bot (the 'tester') to assert that your bot (the 'target') reacts
   to events appropriately. This means you will need to create a second bot account through the
   `Discord Developer's Portal <https://www.discordapp.com/developers/applications>`_ and obtain the
   authorization token. You also have to invite the tester to your discord guild.
3. Refer to the :ref:`example` for the syntax/function calls necessary to build your suite.

Usage
------

The tests can be run in one of two modes: interactive_ and command-line_. In interactive mode, the bot will wait
for you to initiate tests manually. In command-line mode, the bot will join a designated channel, run all designated
tests, and exit with an error code of 0 if all tests were successful (any other number if otherwise). This allows
for automating your test suite, allowing you to implement Continuous Integration on your Discord bot!

.. _interactive:

Interactive
^^^^^^^^^^^

1. Run the bot by running your test suite module directly (called example_tester.py here): ::

       python example_tester.py ${TARGET_NAME} ${TESTER_TOKEN}

2. Go to the channel you want to run your tests in and call the bot using the ``::run`` command. You can designate specific tests to run by name or use ``::run all``

.. seealso::
    run the ``::help`` command for more options.

.. _command-line:

Command-Line
^^^^^^^^^^^^

For command-line you have to designate the ID of the channel you want to run tests in (preceded by the ``-c`` flag). You must also designated which
tests to run (with the ``-r`` flag). Your command should look something like this: ::

    python example_tester.py ${TARGET_NAME} ${TESTER_TOKEN} -c ${CHANNEL_ID} -r all

The program will print test names to the console as it runs them, and then exit.
