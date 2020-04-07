import re
import argparse


def token_arg(token_value: str) -> str:
    """
    Validates the discord token, won't run the bot if the token is not valid.

    Matches to the regex: [\w\d]{24}\.[\w\d]{6}\.[\w\d-_]{27}.
    Thanks to https://github.com/AnIdiotsGuide/Tutorial-Bot/blob/Episode-4/app.js for the regex I used.
    Thanks to https://gist.github.com/mikecharles/9ed3082b10d77d658743 for an example of how this works with argparse

    :param token_value: The string that may be a bot token
    :return token_value: Returns the token_value if the token matches the regex
    :exception ArgumentParseException: Raises the exception if the token_value does not match the regex
    """

    # Regex check
    if not re.match(r"[MN][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}", token_value):
        raise argparse.ArgumentTypeError(
            "must be a correct Discord bot token.".format(token_value)
        )

    # If that passes, the token's value will be returned.
    return token_value
