from dataclasses import dataclass
from typing import Optional


@dataclass
class Course:
    """ Dataclass for keeping track of course information. """

    course_code: str            # COMP 155
    name: str                   # Intro to Computer Science
    credit_hours: int           # 3.0
    year: Optional[int]         # 2017
    semester: Optional[str]     # Fall
    # TODO: requisites field
