"""
The TestCollector Class and some supporting code.

Each test function in the tester bot should be decorated with an instance of TestCollector(),
and must have a unique name. The TestCollector() is then passed onto the bot, which runs the tests.
"""

from .interface import Test


class ExpectCalls:
    """ Wrap a function in an object which counts the number
        of times it was called. If the number of calls is not
        equal to the expected number when this object is
        garbage collected, something has gone wrong, and in
        that case an error is thrown.
    """

    def __init__(self, function, expected_calls=1):
        self.function = function
        self.expected_calls = expected_calls
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        return self.function(*args, **kwargs)

    def __del__(self):
        if self.call_count != self.expected_calls:
            message = (
                "{} was called {} times. It was expected to have been called {} times"
            )
            raise RuntimeError(
                message.format(self.function, self.call_count, self.expected_calls)
            )


class TestCollector:
    """ Used to group tests and pass them around all at once. """

    def __init__(self):
        self._tests = []

    def add(self, function, name: str = "", needs_human: bool = False):
        """ Adds a test function to the group. """
        name = name or function.__name__
        test = Test(name, function, needs_human=needs_human)
        if name in self._tests:
            raise KeyError("A test case called {} already exists.".format(name))
        self._tests.append(test)

    def find_by_name(self, name: str):
        """ Return the test with the given name.
            Return None if it does not exist.
        """
        for i in self._tests:
            if i.name == name:
                return i
        return None

    def __call__(self, *args, **kwargs):
        """ Add a test decorator-style. """

        def _decorator(function):
            self.add(function, *args, **kwargs)

        return ExpectCalls(_decorator, 1)

    def __iter__(self):
        return (i for i in self._tests)
