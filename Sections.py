"""Gets all section-info for a course from Canvas API.

See https://canvas.instructure.com/doc/api/sections.html#method.sections.index for reference
"""
from typing import Dict
from typing import List

from requests import Response

import Canvas_Request


def process_sections(content: Response, sections: List[Dict]) -> None:
    """Pull out course sections.

    Args:
        content (Response): The response object provided by Canvas_Request
        sections (List[Dict]): The list to which we add the sections
    """
    content_dict: Dict = content.json()
    for section in content_dict:
        sections.append(section)


def get_all_sections(course_id: str) -> List[Dict]:
    """Return all sections in a course.

    Args:
        course_id (str): The course id for which you are requesting sections

    Raises:
        Exception: If there are no sections found...

    Returns:
        List[Dict]: The list of sections found
    """
    sections: List[Dict] = []
    r: Response = Canvas_Request.get_endpoint(f"courses/{course_id}/sections")
    process_sections(r, sections)
    while r.links["current"]["url"] != r.links["last"]["url"]:
        r = Canvas_Request.get(r.links["next"]["url"])
        process_sections(r, sections)
    if len(sections) == 0:
        raise Exception("No sections were found?")
    return sections
