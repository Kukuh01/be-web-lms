from ninja import Router, Schema
from .models import Lesson
from typing import List
from core.jwt_auth import JWTAuth
from core.permissions import dosen_only

router = Router(auth=JWTAuth(), tags=["Lessons"])

class LessonIn(Schema):
    course_id: int
    title: str
    content: str

class LessonOut(Schema):
    id: int
    title: str
    content: str

@router.post("/")
def create_lesson(request, data: LessonIn):
    dosen_only(request)
    lesson = Lesson.objects.create(**data.dict())
    return {"id": lesson.id}

@router.get("/course/{course_id}", response=List[LessonOut])
def lessons_by_course(request, course_id: int):
    return Lesson.objects.filter(course_id=course_id)