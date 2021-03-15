from dataclasses import dataclass


@dataclass
class Schedule:
    """ Dataclass for keeping track of schedule information.

    Status Keys::

        1 = Awaiting Advisor Approval
        2 = Awaiting Student Creation
        3 = Awaiting Student Approval
        4 = Approved
    """

    student_id: int
    status: int         # see key in class docs
    courses: list        # list of Course objects

    @property
    def status_str(self) -> str:
        return self.status_int_to_str(self.status)

    @classmethod
    def status_int_to_str(cls, status: int) -> str:
        return {
            1: 'Awaiting Advisor Approval',
            2: 'Awaiting Student Creation',
            3: 'Awaiting Student Approval',
            4: 'Approved'
        }.get(status, 'Unknown')

    @classmethod
    def status_str_to_int(cls, status: str) -> int:
        key = status.lower().replace(' ', '')
        return {
            'awaitingadvisorapproval': 1,
            'awaitingstudentcreation': 2,
            'awaitingstudentapproval': 3,
            'approved': 4
        }.get(key)
