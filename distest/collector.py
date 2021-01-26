"""
The TestCollector Class and some supporting code.

Each test function in the tester bot should be decorated with an instance of TestCollector(),
and must have a unique name. The TestCollector() is then passed onto the bot, which runs the tests.
"""

from .TestInterface import Test


class ExpectCalls:
    """ Wrap a function in an object which counts the number of times it was called. If the number
    of calls is not equal to the expected number when this object is garbage collected, something has
    gone wrong, and in that case an error is thrown.

    :param function function: The test :py:class:`function` to track
    :param int expected_calls: The number of calls expected for that function. Defaults to 1,
                               and is not currently able to be set to another value
    """

    def __init__(self, function, expected_calls=1):
        self.function = function
        self.expected_calls = expected_calls
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        """ Increment ``call_count`` when the function is called, then actually call the function. """
        self.call_count += 1
        return self.function(*args, **kwargs)

    def __del__(self):
        """ Create an error that contains the call information if the call count is wrong when the test is deleted"""
        if self.call_count != self.expected_calls:
            message = (
                "{} was called {} times. It was expected to have been called {} times"
            )
            raise RuntimeError(
                message.format(self.function, self.call_count, self.expected_calls)
            )


class TestCollector:
    """ Used to group tests and pass them around all at once.

    Tests can be either added with :func:`add <distest.collector.TestCollector.add>` or by using ``@TestCollector``
    to decorate the function, as seen in the sample code below. Is very similar in function to
    :py:class:`Command <discord.ext.commands.Command>` from discord.py, which you might already be familiar with.

    .. literalinclude:: ../../../example_tester.py
       :linenos:
       :language: python3
       :lines: 66-77
       :emphasize-lines: 1, 8

    """

    def __init__(self):
        self._tests = []

    def add(self, function, name=None, needs_human=False):
        """ Adds a test function to the group, if one with that name is not already present

        :param func function: The function to add
        :param str name: The name of the function to add, defaults to the function name but can be overridden
                         with the provided name just like with :py:class:`discord.ext.commands.Command`.
                         See sample code above.
        :param bool needs_human: Optional boolean, true if the test requires a human interaction
        """
        name = name or function.__name__
        test = Test(name, function, needs_human=needs_human)
        if name in self._tests:
            raise KeyError("A test case called {} already exists.".format(name))
        self._tests.append(test)

    def find_by_name(self, name):
        """ Return the test with the given name, return ``None`` if it does not exist.

        :param str name: The name of the test
        :rtype: :py:class:`Test <distest.TestInterface.Test>`, none
        """
        for i in self._tests:
            if i.name == name:
                return i
        return None

    def __call__(self, *args, **kwargs):
        """ Add a test decorator-style, simply calls `add` when used to decorate something. """

        def _decorator(function):
            self.add(function, *args, **kwargs)

        return ExpectCalls(_decorator, 1)

    def __iter__(self):
        """ Makes the `TestCollector` able to be iterated over, which is really helpful in a number of cases."""
        return (i for i in self._tests)
