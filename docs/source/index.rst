Distest
=======

Distest makes it easy to write application tests for discord bots.

Distest uses a secondary bot to send commands to your bot and ensure that it responds as expected.

See the :ref:`interface <interface>` reference for a list of assertions this library is capable of.

.. note::
    Two quick note about recent changes:

    1. You NEED to enable the ``members`` intent on the tester bot. For more information, see :ref:`Member Intent <member_intent>`
    2. If you're using the :py:class:`ext.commands.Bot <discord.ext.commands.Bot>` system, you will need to patch your ``Bot`` to allow it to listen to other discord bots, as usually commands ignore other bots. This is really easy, we provide the patching function, just take a look at the :ref:`patching <patches>` documentation page.

.. toctree::
    :maxdepth: 2
    :caption: Getting Started

    usage/quickstart
    usage/example
    distest/member_intent

.. toctree::
    :maxdepth: 2
    :glob:
    :caption: Reference

    distest
    distest/interface
    distest/enums
    distest/bot
    distest/collector
    distest/exceptions

.. toctree::
    :maxdepth: 2
    :caption: Other

    distest/contributing
    distest/member_intent
    distest/patches

Meta Documentation Pages
________________________

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
