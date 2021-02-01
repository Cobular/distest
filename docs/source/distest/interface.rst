.. _interface:

Interface
=========

This is the most important class in the library for you, as it contains all the assertions and tools you need to interface with the library. Generally broken down into a few overall types:

* Message (i.e. :py:meth:`assert_message_contains <distest.TestInterface.assert_message_contains>`): Does not send it's own message, so it require a :py:class:`Message <discord.Message>` to be passed in.
* Reply (i.e. :py:meth:`assert_reply_contains <distest.TestInterface.assert_reply_contains>`): Sends a message containing the text in `contents` and analyzes messages sent after that.
    * Use :py:meth:`get_delayed_reply <distest.TestInterface.get_delayed_reply>` to wait an amount of time before checking for a reply
* Embed (i.e. :py:meth:`assert_embed_equals <distest.TestInterface.assert_embed_equals>`): Sends a message then checks the embed of the response against a list of attributes
* Other Tests (i.e. :py:meth:`ask_human <distest.TestInterface.ask_human>`): Some tests do weird things and don't have a clear category.
* Interface Functions (i.e. :py:meth:`connect <distest.TestInterface.connect>`, :py:meth:`send_message <distest.TestInterface.send_message>`): Help other tests but also can be useful in making custom tests out of the other tests.

-----------------------------------

.. todo::
    Re-organize this file more sensibly

.. autoclass:: distest.TestInterface.TestInterface
    :members:

----------------------------------

.. _test:

.. autoclass:: distest.TestInterface.Test
    :members:
