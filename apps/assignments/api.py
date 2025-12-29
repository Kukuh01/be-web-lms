from ninja import Router, Schema
from .models import Assignment
from datetime import datetime
from typing import List
from core.jwt_auth import JWTAuth
from core.permissions import dosen_only

router = Router(auth=JWTAuth(), tags=["Assignment"])

class AssignmentIn(Schema):
    lesson_id: int
    title: str
    description: str
    deadline: datetime

class AssignmentOut(Schema):
    id: int
    lesson_id: int
    title: str
    description: str
    deadline: datetime

@router.post("/")
def create_assignment(request, data: AssignmentIn):
    dosen_only(request)
    assignment = Assignment.objects.create(**data.dict())
    return {"id": assignment.id}

@router.get("/lesson/{lesson_id}",  response=List[AssignmentOut])
def list_assignments(request, lesson_id: int):
    return Assignment.objects.filter(lesson_id=lesson_id)