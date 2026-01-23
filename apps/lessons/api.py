from ninja import Router, Schema
from typing import List
from core.jwt_auth import JWTAuth
from core.permissions import dosen_or_admin_only
from .services import LessonService
from .schemas import LessonIn, LessonOut

router = Router(auth=JWTAuth(),tags=["Lessons"])
lesson_service = LessonService()

@router.get("/course/{course_id}", response=List[LessonOut])
def lessons_by_course(request, course_id: int):
    return lesson_service.get_lessons_by_course(course_id)

@router.post("/{course_id}/lessons", response={201: LessonOut})
def create_lesson(request, course_id: int, data: LessonIn):
    dosen_or_admin_only(request)
    lesson = lesson_service.create_lesson(course_id, **data.dict())
    return 201, lesson

@router.put("/{lesson_id}", response={200: LessonOut})
def update_lesson(request, lesson_id: int, data: LessonIn):
    dosen_or_admin_only(request)
    lesson = lesson_service.update_lesson(lesson_id, **data.dict())
    return 200, lesson

@router.delete("/{lesson_id}")
def delete_lesson(request, lesson_id: int):
    dosen_or_admin_only(request)
    lesson_service.delete_lesson(lesson_id)
    return 200, {
        "success": True,
        "message": "Lesson berhasil dihapus"
    }