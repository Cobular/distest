from discord import Message, Embed
from typing import Dict

from distest.exceptions import ResponseDidNotMatchError

import re


async def assert_embed_equals(
    message: Message, matches: Embed, attributes_to_prove: list = None,
):
    """If ``matches`` doesn't match the embed of ``message``, fail the test.

    Checks only the attributes from ``attributes_to_prove``.

    :param message: original message
    :param matches: :py:class:`embed <discord.Embed>` object to compare to
    :param attributes_to_prove: a string list with the attributes of the embed, which are to compare
        This are all the Attributes you can prove: "title", "description", "url", "color",
        "author", "video", "image" and "thumbnail".
    :return: message
    :rtype: discord.Message
    """

    # All possible attributes a user can set during initialisation
    possible_attributes = [
        "title",
        "description",
        "url",
        "color",
        "author",  # This is not the original author of the message, author is a attribute you are able to set.
        "video",
        "image",
        "thumbnail",
    ]
    # View all (visible) attributes visualized here: https://imgur.com/a/tD7Ibc4

    attributes = []

    # Proves, if the attribute provided by the user is a valid attribute to check
    if attributes_to_prove is not None:
        for value in attributes_to_prove:
            if value not in possible_attributes:
                raise NotImplementedError('"' + value + '" is not a possible value.')
            attributes.append(value)
    else:
        # If no attributes to check are provided, check them all.
        attributes = possible_attributes

    for embed in message.embeds:
        for attribute in attributes:
            if attribute == "image" or attribute == "thumbnail":
                # Comparison of Embedded Images / Thumbnails
                if getattr(getattr(embed, attribute), "url") != getattr(
                    getattr(matches, attribute), "url"
                ):
                    raise ResponseDidNotMatchError(
                        "The {} attribute did't match".format(attribute)
                    )
            elif attribute == "video":
                # Comparison of Embedded Video
                if getattr(getattr(embed, "video"), "url") != getattr(
                    getattr(matches, "video"), "url"
                ):
                    raise ResponseDidNotMatchError("The video attribute did't match")
            elif attribute == "author":
                # Comparison of Author
                if getattr(getattr(embed, "author"), "name") != getattr(
                    getattr(matches, "author"), "name"
                ):
                    raise ResponseDidNotMatchError("The author attribute did't match")
            elif not getattr(embed, attribute) == getattr(matches, attribute):
                print(
                    "Did not match:",
                    attribute,
                    getattr(embed, attribute),
                    getattr(matches, attribute),
                )
                raise ResponseDidNotMatchError
    return message


async def assert_embed_regex(message: Message, patterns: Dict[str, str]):
    """If regex patterns ``patterns`` cannot be found in the embed of ``message``, fail the test.

    Checks only the attributes from the dictionary keys of ``patterns``.

    :param message: original message
    :param patterns: a dict with keys of the attributes and regex values.
    :return: message
    :rtype: discord.Message
    """

    possible_attributes = [
        "title",
        "description",
        "color",
    ]

    for embed in message.embeds:
        for attribute, regex in patterns.items():
            if not re.search(regex, getattr(embed, attribute)):
                print(
                    "Regex did not match:",
                    attribute,
                    getattr(embed, attribute),
                    regex,
                )
                raise ResponseDidNotMatchError
    return message
