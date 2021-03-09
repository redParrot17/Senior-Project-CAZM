from dataclasses import dataclass


@dataclass
class Schedule:
    """ Dataclass for keeping track of schedule information.

    Status Keys::

        1 = Approved
        2 = Awaiting Student Approval
        3 = Awaiting Student Creation
        4 = Awaiting Advisor Approval
    """

    schedule_id: int
    student_id: int
    status: int         # see key in class docs
    courses = []        # list of Course objects

    @property
    def status_str(self) -> str:
        return self.status_int_to_str(self.status)

    @classmethod
    def status_int_to_str(cls, status: int) -> str:
        return {
            1: 'Approved',
            2: 'Awaiting Student Approval',
            3: 'Awaiting Student Creation',
            4: 'Awaiting Advisor Approval'
        }.get(status, 'Unknown')

    @classmethod
    def status_str_to_int(cls, status: str) -> int:
        key = status.lower().replace(' ', '')
        return {
            'approved': 1,
            'awaitingstudentapproval': 2,
            'awaitingstudentcreation': 3,
            'awaitingadvisorapproval': 4
        }.get(key)
