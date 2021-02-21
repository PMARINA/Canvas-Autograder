"""Manage config file to store state.

config file: stores in a dict:
    course, section, assignment

The keys for which (dict -- key:value) are located in Variables.py
"""
import os
import pickle
from typing import Dict

import Variables


def exists(config_filepath: str = Variables.CONFIG_FILE) -> bool:
    """Check if config file exists on disk.

    Args:
        config_filepath (str, optional): The location of the config file, default in Variables.py . Defaults to Variables.CONFIG_FILE.

    Returns:
        bool: Whether or not the config file exists (True: exists)
    """
    abs_config_fp: str = os.path.abspath(config_filepath)
    return os.path.exists(abs_config_fp)


def load(config_filepath: str = Variables.CONFIG_FILE) -> Dict:
    """Return the saved state.

    Args:
        config_filepath (str, optional): Location on disk to config file. Defaults to Variables.CONFIG_FILE.

    Raises:
        EnvironmentError: If the config file is not found

    Returns:
        Dict: The stored configuration in the predefined format (see top)
    """
    abs_config_fp = os.path.abspath(config_filepath)
    if not os.path.exists(abs_config_fp):
        errmsg = f"Config file not found at {abs_config_fp}. "
        raise EnvironmentError(errmsg)
    conf_dict = None
    with open(abs_config_fp, "rb") as f:
        conf_dict = pickle.load(f)
    return conf_dict


def save(
    course: Dict,
    section: Dict,
    assignment: Dict,
    config_filepath: str = Variables.CONFIG_FILE,
) -> None:
    """Save the given parameters to disk in a dict.

        The keys for all are in Variables.py
    Args:
        course (str): The course being graded
        section (str): The section being graded
        assignment (str): The assignment being graded
        config_filepath (str, optional): The location of the config file (preset in Variables.py). Defaults to Variables.CONFIG_FILE.
    """
    state: Dict = {}
    state[Variables.COURSE_KEY] = course
    state[Variables.SECTION_KEY] = section
    state[Variables.ASSIGNMENT_KEY] = assignment
    abs_config_fp: str = os.path.abspath(config_filepath)
    with open(abs_config_fp, "wb") as f:
        pickle.dump(state, f)
