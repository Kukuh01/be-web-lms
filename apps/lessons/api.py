from ninja import Router, Schema
from .models import Lesson

router = Router()

class LessonIn(Schema):
    course_id: int
    title: str
    content: str

@router.post("/")
def create_lesson(request, data: LessonIn):
    lesson = Lesson.objects.create(**data.dict())
    return {"id": lesson.id}

@router.get("/course/{course_id}")
def lessons_by_course(request, course_id: int):
    return Lesson.objects.filter(course_id=course_id)