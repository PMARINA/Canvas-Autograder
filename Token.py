"""Handles the user token for making authenticated requests to the canvas api."""
import os
import pickle

import pyperclip  # type: ignore
from loguru import logger

import Canvas_Request
import Variables


token_fp: str = os.path.abspath(Variables.TOKEN_FILE)
token_string: str = ""


def verify() -> None:
    """Save token if none found. Verify new or existing token by requesting the list of courses available.

    Raises:
        ValueError: Using the token results in a non-ok http status code
    """
    global token_fp, token_string
    if not os.path.exists(token_fp):
        error_msg: str = f"Token was not found at {token_fp}"
        logger.info(error_msg)
        input("Please copy the token. When ready, please hit enter. >>> ")
        token_string = pyperclip.paste().strip()
        with open(token_fp, "wb") as f:
            pickle.dump(token_string, f)
        logger.success(f"Saved token to {token_fp}. Exiting")
    stat_code: int = Canvas_Request.get_endpoint("courses").status_code
    if stat_code != 200:
        raise ValueError(
            (
                "Canvas server indicates a bad token."
                f" Please delete {token_fp} and try again."
            ),
        )


def load() -> None:
    """Load the Canvas Token from disk (only useful for Canvas_Request).

    Raises:
        EnvironmentError: The token was not found but explicitly requested
    """
    global token_fp, token_string
    if not os.path.exists(token_fp):
        error_msg: str = f"Token was not found at {token_fp}"
        raise EnvironmentError(error_msg)
    with open(token_fp, "rb") as f:
        token_string = pickle.load(f)


def get() -> str:
    """Return the token. Uses load only if not already in memory to avoid excessive disk-reading, thus the first call might be slightly slower than subsequent.

    Returns:
        str: The user's token
    """
    global token_string
    if token_string == "":
        load()
    return token_string
