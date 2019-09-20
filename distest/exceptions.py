"""
Stores all the Exceptions that can be called during testing.

Allows for a more through understanding of what went wrong. Not all of these are currently in use.
"""


class TestRequirementFailure(Exception):
    """ Base class for the special errors that are raised when an expectation is not met during testing """


class NoResponseError(TestRequirementFailure):
    """ Raised when the target bot fails to respond to a message """


class NoReactionError(TestRequirementFailure):
    """ Raised when the target bot failed to react to a message """


class UnexpectedResponseError(TestRequirementFailure):
    """ Raised when the target bot failed to stay silent """


class ErrordResponseError(TestRequirementFailure):
    """ Raised when the target bot produced an error message """


class UnexpectedSuccessError(TestRequirementFailure):
    """ Raised when the target bot failed to produce an error message """


class HumanResponseTimeout(TestRequirementFailure):
    """ Raised when a human fails to assert the result of a test """


class HumanResponseFailure(TestRequirementFailure):
    """ Raised when a human fails a test """


class ResponseDidNotMatchError(TestRequirementFailure):
    """ Raised when the target bot responds with a message that doesn't meet criteria """


class ReactionDidNotMatchError(TestRequirementFailure):
    """ Raised when the target bot reacts with the wrong emoji """
