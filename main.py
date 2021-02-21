"""Run this file for running the project. See README for all info."""
from typing import Any
from typing import Dict
from typing import List

import Assignments
import Config
import Courses
import Question
import Sections
import Token
import Variables

# Defined through global below...
course: Dict[Any, Any] = {}
section: Dict[Any, Any] = {}
assignment: Dict[Any, Any] = {}


def load_config() -> None:
    """Load pre-existing config from `Config.load`."""
    global course, section, assignment
    conf_dict: Dict[str, Dict] = Config.load()
    course = conf_dict[Variables.COURSE_KEY]
    section = conf_dict[Variables.SECTION_KEY]
    assignment = conf_dict[Variables.ASSIGNMENT_KEY]


def save_config() -> None:
    """Save the current state to a config file `Config.save`."""
    global course, section, assignment
    Config.save(course, section, assignment)


def want_continue_previous_session() -> bool:
    """Ask the user if they would like to continue an existing session (don't re-prompt for course, section, assignment).

    Returns:
        bool: What the user wants: Yes: True...
    """
    return Question.askyN("Would you like to continue the previous session?")


def select_course() -> None:
    """Get all the courses the user has access to and ask which they would like to grade."""
    global course
    courses: List[Dict[Any, Any]] = Courses.get_all_courses()
    courses = sorted(courses, key=lambda x: x["name"], reverse=True)
    course = Question.select_option(courses, "course")


def select_section() -> None:
    """Ask the user if they would like to focus on a certain section, if yes, pick the section.

    Raises:
        ValueError: The course must be initialized to select a section (sub-property)
    """
    global course, section
    if not course:
        raise ValueError("course has not been initialized")

    if Question.askYn("Would you like to filter by section?"):
        sections: List[Dict[Any, Any]] = Sections.get_all_sections(course["id"])
        section = Question.select_option(sections, "section")


def select_assignment() -> None:
    """Ask user to pick an assignment from their class/section (section is optional).

    Raises:
        ValueError: The course must be selected to pick assignment (sub-property)
    """
    global course, section, assignment
    if not course:
        raise ValueError("course has not been initialized")

    def key_for_sorting_section(a: Dict) -> int:
        """Get the number of ungraded submissions given an assignment (after matching section).

        Args:
            a (Dict): Dict with 'needs_grading_count_by_section' dict, which has 'section_id' and 'needs_grading_count'

        Returns:
            int: the number of ungraded submissions
        """
        global section
        for gcs in a["needs_grading_count_by_section"]:
            if gcs["section_id"] == section["id"]:
                return gcs["needs_grading_count"]
        return -1

    if not section:
        assignments: List[Dict[Any, Any]] = Assignments.get_all_assignments(
            course["id"],
        )
        assignments = sorted(
            assignments, key=lambda a: a["needs_grading_count"], reverse=True,
        )

        def add_ungraded_count(assignment: Dict) -> None:
            ungraded_count: str = assignment["needs_grading_count"]
            assignment["name"] += f" ({ungraded_count})"

        assignments = list(map(add_ungraded_count, assignments))

    else:
        assignments = Assignments.get_all_assignments(
            course["id"], section["id"],
        )
        assignments = sorted(
            assignments, key=key_for_sorting_section, reverse=True,
        )

        def add_ungraded_count(assignment: Dict) -> None:
            assignment["name"] += f" ({key_for_sorting_section(assignment)})"

        assignments = list(map(add_ungraded_count, assignments))
    assignment = Question.select_option(assignments, "assignment")


def setup_initial_state() -> None:
    """Verify token, check if user wants to load the config, or otherwise sets the necessary attributes to begin grading."""
    Token.verify()
    if Config.exists() and want_continue_previous_session():
        load_config()
    else:
        select_course()
        select_section()
        select_assignment()
        save_config()


def main() -> None:
    """Run the project..."""
    setup_initial_state()


if __name__ == "__main__":
    main()
