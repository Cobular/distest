from distest.exceptions import ReactionDidNotMatchError


async def assert_reaction_equals(self, contents, emoji):
    """ Send a message and ensure that the reaction is equal to `emoji`. If not, fail the test.

    :param str contents: The content of the trigger message. (A command)
    :param discord.Emoji emoji: The emoji that the reaction must equal.
    :returns: The resultant reaction object.
    :rtype: discord.Reaction
    :raises: ReactionDidNotMatchError
    """
    reaction = await self.wait_for_reaction(await self.send_message(contents))
    if str(reaction[0].emoji) != emoji:
        raise ReactionDidNotMatchError
    return reaction
