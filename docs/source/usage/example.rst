.. _example:

Example Test Suite
==================

This is the ``example_tester.py`` file found in the root directory. It contains tests for every assertion in :ref:`interface`. This suite is also used to test our library, in conjunction with the ``example_target.py``.
The easiest way to get started is to adapt this suite of tests so it's specific to your bot, then run this module with

  .. code-block:: console

     $ python example_tester.py ${TARGET_NAME} ${TESTER_TOKEN}

where ``TARGET_NAME`` is the display name of your discord bot, and ``TESTER_TOKEN`` is the auth token for your testing bot.

.. literalinclude:: ../../../example_tester.py
   :linenos:
   :language: python3
