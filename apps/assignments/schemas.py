from datetime import datetime
from typing import List
from ninja import Schema
from apps.submissions.schemas import SubmissionResponse

class AssignmentIn(Schema):
    title: str
    description: str
    deadline: datetime

class AssignmentOut(Schema):
    id: int
    lesson_id: int
    title: str
    description: str
    deadline: datetime
    submissions: List[SubmissionResponse] = [] 

    @staticmethod
    def resolve_submissions(obj):
        # Mengambil semua submission terkait assignment ini
        return obj.submission_set.all()