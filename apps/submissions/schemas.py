from ninja import Schema
from typing import Optional
from datetime import datetime

class SubmissionResponse(Schema):
    id: int
    file_url: str
    lastModified: Optional[datetime] = None
    grade: Optional[float] = None
    student_name: str

class ErrorSchema(Schema):
    detail: str

class GradeIn(Schema):
    grade: float

class SuccessSchema(Schema):
    success: bool
    message: str