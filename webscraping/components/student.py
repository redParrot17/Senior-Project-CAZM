from dataclasses import dataclass


@dataclass
class Student:
    """ Class for keeping track of information about a student. """

    student_id: int
    advisor_id: int
    firstname: str
    lastname: str
    email: str              # 'example@college.edu'
    majors: list            # [('major_name1', major_year1), ('major_name2', major_year2)]
    classification: str     # 'Freshman' or 'Junior' or 'Senior' etc
    graduation_year: int
