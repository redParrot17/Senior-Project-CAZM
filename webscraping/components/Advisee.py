from dataclasses import dataclass


@dataclass
class Advisee:
    """ Class for keeping track of information about an advisee. """

    student_id: int
    advisor_id: int
    firstname: str
    lastname: str
    email: str
    major: str
    classification: str
    graduation_year: int
