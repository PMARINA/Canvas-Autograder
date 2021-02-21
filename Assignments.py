"""Handles getting assignments from Canvas API.

Reference for Canvas: https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index
"""
from typing import Dict
from typing import List

from requests import Response

import Canvas_Request


def process_assignments(
    content: Response, assignments: List[Dict], section_id: str = "",
) -> None:
    """Add all assignments from response to list.

    Args:
        content (Response): response object from the api call
        assignments (List[Dict]): Add all assignments found to this list
        section_id (str): If you want to only add assignments from a single section. Defaults to "".
    """

    def is_section_with_gradable(sec_info: Dict) -> bool:
        """Return if the section filter will select this section and if the section has any gradable assignments.

        Args:
            sec_info (Dict): The dict containing the section string and number of gradable submissions

        Returns:
            bool: If the assignment has your section with gradable assignments
        """
        if sec_info["section_id"] == section_id:
            if sec_info["needs_grading_count"] > 0:
                return True
        return False

    content_dict: Dict = content.json()
    for assignment in content_dict:
        if not section_id:
            if assignment["needs_grounding_count"] > 0:
                assignments.append(assignment)
        else:
            for sec_info in assignment["needs_grading_count_by_section"]:
                if is_section_with_gradable(sec_info):
                    assignments.append(assignment)


def get_all_assignments(course_id: str, section_id: str = "") -> List[Dict]:
    """Return all assignments in the course, and optionally, filters by section_id.

    Args:
        course_id (str): The course id for which you wish to acquire assignments
        section_id (str): The section id you wish to filter by ("" for no filtering)

    Raises:
        Exception: If no gradable assignments are found...

    Returns:
        List[Dict]: A list of all assignments that match your query. See Canvas API for details of dict.
    """
    assignments: List[Dict] = []
    r: Response
    if not section_id:
        r = Canvas_Request.get_endpoint(f"courses/{course_id}/assignments")
    else:
        section_urlquery = "needs_grading_count_by_section=True"
        url: str = f"courses/{course_id}/assignments?{section_urlquery}"
        r = Canvas_Request.get_endpoint(url)
    process_assignments(r, assignments, section_id)
    while r.links["current"]["url"] != r.links["last"]["url"]:
        r = Canvas_Request.get(r.links["next"]["url"])
        process_assignments(r, assignments, section_id)
    if len(assignments) == 0:
        errmsg = (
            "No gradable assignments found under your Canvas user."
            " Are you a 'ta' or 'teacher'?"
        )
        raise Exception(errmsg)
    return assignments
