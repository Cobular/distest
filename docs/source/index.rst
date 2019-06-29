Welcome to Distest's documentation!
===================================

Distest is a library that makes it very easy to write great application tests for your discord bots! See :ref:`quickstart <quickstart>` for information on how to get started fast!

Distest works by using a secondary Discord bot account to send specified commands to your bot and ensure that it reacts appropriately. Without Distest,
you would have to mock a discord server to properly test your bot. With Distest, you can automate the testing of your bot using a shell script, making
testing and continous integration painless and easy.

See the :ref:`interface <interface>` reference for a list of assertions this library is capable of. If you can think of an assertion that would be useful, make a pull request!

.. toctree::
    :maxdepth: 2
    :caption: Getting Started

    usage/quickstart
    usage/example

.. toctree::
    :maxdepth: 2
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

    distest/getting-started-documentation

Meta Documentation Pages
========================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
