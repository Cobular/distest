.. _enums:

Enumerations
============

The following enumeration (subclass of :py:class:`enum.Enum`) is used to indicate the result of a run test.

.. class:: TestResult

   Specifies the result of a test.

   .. attribute:: UNRUN

      Test has not been run in this session

   .. attribute:: SUCCESS

      Test succeeded

   .. attribute:: FAILED

      Test has failed.
