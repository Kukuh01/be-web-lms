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

class SuccessSchema(Schema):
    success: bool
    message: str