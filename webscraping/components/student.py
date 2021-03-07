from dataclasses import dataclass


@dataclass
class Student:
    """ Dataclass for keeping track of student information. """

    student_id: int
    advisor_id: int
    firstname: str
    lastname: str
    email: str                  # 'example@college.edu'
    majors: list                # [('major_name1', major_year1), ('major_name2', major_year2)]
    classification: str         # 'Freshman' or 'Junior' or 'Senior' etc
    graduation_year: int
    graduation_semester: str
    enrolled_year: int
    enrolled_semester: str
    credits_completed: int = 0  # This is a calculated value and cannot be manually set
