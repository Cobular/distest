.. _quickstart:

Quickstart
==========

Installation
------------

1. Install the library with pip:
     .. code-block:: console

        $ pip install distest

2. Distest works by using a second bot (the 'tester') to assert that your bot (the 'target') reacts
   to events appropriately. This means you will need to create a second bot account through the
   `Discord Developer's Portal <https://www.discordapp.com/developers/applications>`_ and obtain the
   authorization token. You also have to invite the tester to your discord guild.
3. Refer to the :ref:`example` for the syntax/function calls necessary to build your suite.

Usage
------

The tests can be run in one of two modes: interactive_ and command-line_. In interactive mode, the bot will wait
for you to initiate tests manually. In command-line mode, the bot will join a designated channel, run all designated
tests, and exit with a code of 0 if all tests were successful and any other number if the one or more tests failed.
This allows for automating your test suite, allowing you to implement Continuous Integration on your Discord bot!

No matter how you run your tester, the file must contain:

1. A call to :py:meth:`run_dtest_bot <distest.run_dtest_bot>`, which will handle all command line arguments and run the tester in the correct mode
2. A :py:meth:`TestCollector <distest.collector.TestCollector>`, which will let the bot find and run the you specify
3. One or more :py:meth:`Test <distest.interface.Test>`, which should be decorated with the :py:meth:`TestCollector <distest.collector.TestCollector>`, and are the actual tests that are run.

.. note::
    The error codes will currently be 0 on success or 1 on failure, but we plan to implement meaningful error codes

.. _interactive:

Interactive Mode
^^^^^^^^^^^^^^^^

1. Run the bot by running your test suite module directly (called example_tester.py here):
     .. code-block:: console

        $ python example_tester.py TARGET_NAME TESTER_TOKEN

2. Go to the channel you want to run your tests in and call the bot using the ``::run`` command. You can either designate specific tests to run by name or use ``::run all``

.. seealso::

    ``::help`` command for more commands/options.

.. _command-line:

Command-Line Mode
^^^^^^^^^^^^^^^^^

For command-line you have to designate the ID of the channel you want to run tests in (preceded by the ``-c`` flag). You must also designate which
tests to run (with the ``-r`` flag). Your command should look something like this:

  .. code-block:: console

     $ python example_tester.py TARGET_NAME TESTER_TOKEN -c CHANNEL_ID -r all

The program will print test names to the console as it runs them, and then exit.

.. seealso::
    ``readme.md`` on GitHub, which contains a more in-depth look at the command properties
