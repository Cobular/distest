from concurrent.futures import _base
from asyncio.exceptions import TimeoutError, CancelledError
from discord import Reaction
from distest.exceptions import (
    UnexpectedResponseError,
    HumanResponseTimeout,
    HumanResponseFailure,
)


async def ensure_silence(self):
    """ Assert that the bot does not post any messages for some number of seconds.

    :raises: UnexpectedResponseError, TimeoutError
    """
    try:
        await self.client.wait_for(
            "message", timeout=self.client.timeout, check=self._check_message
        )
    except (_base.TimeoutError, TimeoutError, CancelledError):
        pass
    else:
        raise UnexpectedResponseError


async def ask_human(self, query):
    """ Ask a human for an opinion on a question using reactions.

    Currently, only yes-no questions are supported. If the human answers 'no', the test will be failed. Do not use
    if avoidable, since this test is not really automateable. Will fail if the reaction is wrong or takes too long
    to arrive

    :param str query: The question for the human.
    :raises: HumanResponseTimeout, HumanResponseFailure
    """
    message = await self.send_message(query)
    await message.add_reaction("\u2714")
    await message.add_reaction("\u274C")

    def check(human_reaction, user):
        if human_reaction.count > 1:
            return human_reaction.message

    try:
        reaction: Reaction = await self.client.wait_for(
            "reaction_add", timeout=self.client.timeout, check=check
        )
    except _base.TimeoutError:
        raise HumanResponseTimeout
    else:
        reaction, _ = reaction
        if reaction.emoji == "\u274c":
            raise HumanResponseFailure
