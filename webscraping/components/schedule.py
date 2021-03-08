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
    def status_str(self):
        return {
            1: 'Approved',
            2: 'Awaiting Student Approval',
            3: 'Awaiting Student Creation',
            4: 'Awaiting Advisor Approval'
        }.get(self.status, 'Unknown')
