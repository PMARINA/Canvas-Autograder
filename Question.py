"""Handles all User-facing questioning."""
from typing import Callable
from typing import Dict
from typing import List
from typing import Union

from loguru import logger


def default_prompt(category: str) -> str:
    """Create the user prompt for selecting categories of options.

    Args:
        category (str): The type of thing being selected (assignment, section, etc)

    Returns:
        str: The user prompt
    """
    return f"Which {category} would you like to grade? >>> "


def askyN(question: str) -> bool:
    """Asks the user a y/n question with default option No.

    Args:
        question (str): The question the user should be asked

    Returns:
        bool: The user's response (yes: True)
    """
    answer: bool = input(f"{question} [y/N]>>> ").lower().strip().startswith(
        "y",
    )
    return answer


def askYn(question: str) -> bool:
    """Asks the user a y/n question with default option yes.

    Args:
        question (str): The question the user should be asked

    Returns:
        bool: The user's response (yes: True)
    """
    user_answer: str = input(f"{question} [Y/n]>>> ")
    answer: bool = not user_answer.lower().strip().startswith("n")
    return answer


def select_option(
    list_of_options: List[Dict],
    category: str,
    prompt: Union[Callable] = default_prompt,
) -> Dict:
    """Given a list of dicts, each of which has a 'name' attribute, asks the user to select one.

    Args:
        list_of_options (List[Dict]): The list of options from which the user selects. Each element must have a 'name' attribute
        category (str): The category, which is fed into the prompt method/lambda
        prompt (Union[Callable], optional): The prompt for the user to know what they are picking for. Defaults to grading-related prompt. Can be `lambda cat: cat` for direct usage of category name. Defaults to default_prompt.

    Raises:
        ValueError: If the lists have no options for the user to select from.

    Returns:
        Dict: The dict selected by the user
    """
    if len(list_of_options) == 0:
        raise ValueError("No options provided for user's selection")
    if len(list_of_options) == 1:
        return list_of_options[0]
    counter = 1
    for option in list_of_options:
        op_name: str = option["name"]
        print(f"{counter}: {op_name}")
        counter += 1
    done: bool = False
    sel_index: int = -1
    while not done:
        try:
            sel_index = int(input(prompt(category)))
            done = sel_index <= len(list_of_options) and sel_index > 0
            if not done:
                logger.error("selection out of bounds")
        except Exception:
            logger.error("Invalid index (please select 1-N)")
    return list_of_options[sel_index - 1]
