from ninja import Schema
from typing import Optional
from apps.assignments.schemas import AssignmentOut

class LessonIn(Schema):
    title: str
    description: Optional[str] = None
    content: str

class LessonOut(Schema):
    id: int
    title: str
    description: Optional[str] = None
    content: str
    assignment: Optional[AssignmentOut] = None
    @staticmethod
    def resolve_assignment(obj):
        # Mengambil assignment pertama (karena logic 1 Lesson = 1 Assignment)
        # Gunakan getattr untuk menghindari error jika assignment_set belum diprefetch
        if hasattr(obj, 'assignment_set'):
            return obj.assignment_set.first()
        return None