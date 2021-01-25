.. _patches:
.. py:currentmodule:: distest.patches

Patches
========

Contains the code required to patch out the fact that :py:class:`Bot <discord.ext.commands.Bot>` class ignores messages
from other bots.

This should be used if you have a target bot that uses the :py:class:`ext.commands.Bot <discord.ext.commands.Bot>`
system, as otherwise it's commands will ignore messages from the tester bot.


Usage
*****
Simply put the below code into your **main bot** and then when testing, the bot will no longer ignore other bots!

  .. code-block:: python
    :linenos:

    bot = commands.Bot(command_prefix='$')

    # Do anything you want for this if, be it env vars, command line args, or the likes.
    if sys.argv[2] == "TESTING":
        from distest.patches import patch_target
        bot = patch_target(bot)


Docs
****

.. autofunction:: patch_target