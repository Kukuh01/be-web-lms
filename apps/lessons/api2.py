from ninja import Router, Schema
from .models import Lesson
from typing import List, Optional
from core.jwt_auth import JWTAuth
from core.permissions import dosen_only
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .models import Course
from core.permissions import dosen_or_admin_only
from apps.assignments.api import AssignmentOut

router = Router(auth=JWTAuth(),tags=["Lessons"])

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

@router.get("/course/{course_id}", response=List[LessonOut])
def lessons_by_course(request, course_id: int):
    # Optimization: Prefetch berjenjang SANGAT PENTING di sini
    # Course -> Lessons -> Assignment -> Submissions -> Student
    return get_object_or_404(
        Course.objects.prefetch_related(
            "lessons",
            "lessons__assignment_set", # Relasi reverse foreign key dari Assignment
            "lessons__assignment_set__submission_set", # Relasi reverse dari Submission
            "lessons__assignment_set__submission_set__student" # Relasi ke Mahasiswa
        ), 
        id=course_id
    )

@router.post("/{course_id}/lessons", response=LessonOut)
def create_lesson(request, course_id: int, payload: LessonIn):
    dosen_or_admin_only(request)
    course = get_object_or_404(Course, id=course_id)
    lesson = Lesson.objects.create(course=course, **payload.dict())
    return lesson

@router.put("/{lesson_id}", response=LessonOut)
def update_lesson(request, lesson_id: int, payload: LessonIn):
    dosen_or_admin_only(request)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    for attr, value in payload.dict().items():
        setattr(lesson, attr, value)
    lesson.save()
    return lesson

@router.delete("/{lesson_id}")
def delete_lesson(request, lesson_id: int):
    dosen_or_admin_only(request)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.delete()
    return {"success": True}

