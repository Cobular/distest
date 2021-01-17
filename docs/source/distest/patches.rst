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

  .. code-block:: python
    :linenos:

    bot = commands.Bot("r!")
    if os.env.get("TESTING"):
        bot = patch_target(bot)
    # Do stuff


Docs
****

.. autofunction:: patch_target