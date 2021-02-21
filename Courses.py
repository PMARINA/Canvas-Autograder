"""Gets all courses through Canvas API.

https://canvas.instructure.com/doc/api/courses.html#method.courses.index
"""
from typing import Dict
from typing import List

from requests import Response

import Canvas_Request


def process_courses(content: Response, courses: List[Dict]) -> None:
    """Extract all courses from Response content.

    Args:
        content (Response): The response object returned from Canvas_Request
        courses (List[Dict]): The list of course objects (as defined by Canvas' API)
    """
    content_dict = content.json()
    for course in content_dict:
        if (course["enrollments"][0]["type"]).lower() in ["ta", "teacher"]:
            courses.append(course)


def get_all_courses() -> List[Dict]:
    """Get all the gradable courses under a user.

    Raises:
        Exception: If no gradable courses are found for a user

    Returns:
        List[Dict]: The list of gradable courses
    """
    courses: List[Dict] = []
    r: Response = Canvas_Request.get_endpoint("courses")
    process_courses(r, courses)
    while r.links["current"]["url"] != r.links["last"]["url"]:
        r = Canvas_Request.get(r.links["next"]["url"])
        process_courses(r, courses)
    if len(courses) == 0:
        errmsg: str = "No gradable courses found under your Canvas user." " Are you a 'ta' or 'teacher'"
        raise Exception(errmsg)
    return courses


if __name__ == "__main__":
    print(get_all_courses())
