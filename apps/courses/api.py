from ninja import Router, Schema, Form, File
from ninja.files import UploadedFile
from typing import Optional, List
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

# Import Models
from .models import Course
from apps.assignments.models import Assignment
from apps.submissions.models import Submission
from datetime import datetime
from apps.lessons.api import LessonOut

# Auth & Permissions
from core.jwt_auth import JWTAuth
from core.permissions import dosen_only, dosen_or_admin_only

router = Router(auth=JWTAuth(), tags=["Courses Management"])

# ==========================================
# 1. SCHEMAS (Hierarki Data)
# ==========================================

# --- Course Schema ---
class InstructorOut(Schema):
    id: int
    name: str

class CourseIn(Schema):
    title: str
    description: str
    instructor_id: int

class CourseOut(Schema):
    id: int
    title: str
    description: Optional[str]
    linkMeet: Optional[str] = None
    linkWa: Optional[str] = None
    instructor: InstructorOut
    thumbnail: Optional[str] = None
    lessons: List[LessonOut] = []

class CourseDetail(CourseOut):
    lessons: List[LessonOut]

# ==========================================
# 2. CONTROLLERS
# ==========================================

# --- COURSE ENDPOINTS ---

@router.get("/", response=List[CourseOut])
def list_courses(request):
    # Optimization: Select related untuk instructor agar tidak N+1 Query
    return Course.objects.select_related("instructor")\
            .prefetch_related(
                "lessons", 
                "lessons__assignment_set",               # Ambil Assignment
                "lessons__assignment_set__submission_set", # Ambil Submission di dalam Assignment
                "lessons__assignment_set__submission_set__student", # Ambil Data Mahasiswa (untuk nama/NIM)
            ).all()

@router.get("/{course_id}", response=CourseDetail)
def get_course(request, course_id: int):
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

@router.post("/", response=CourseOut)
def create_course(
    request,
    title: str = Form(...),
    description: str = Form(...),
    instructor_id: int = Form(...),
    linkMeet: str = Form(None),
    linkWa: str = Form(None),
    thumbnail: UploadedFile = File(None),
):
    dosen_only(request)
    course = Course.objects.create(
        title=title,
        description=description,
        instructor_id=instructor_id,
        linkMeet=linkMeet,
        linkWa=linkWa,
        thumbnail=thumbnail
    )
    return course

@router.put("/{course_id}", response=CourseOut)
def update_course(
    request,
    course_id: int,
    title: str = Form(...),
    description: str = Form(...),
    instructor_id: int = Form(...),
    linkMeet: str = Form(None),
    linkWa: str = Form(None),
    thumbnail: Optional[UploadedFile] = File(None),
):
    dosen_or_admin_only(request)
    course = get_object_or_404(Course, id=course_id)

    course.title = title
    course.description = description
    course.instructor_id = instructor_id
    course.linkMeet = linkMeet
    course.linkWa = linkWa

    if thumbnail:
        # Hapus file lama jika ada (opsional, tergantung kebutuhan)
        if course.thumbnail:
            course.thumbnail.delete(save=False)
        course.thumbnail = thumbnail

    course.save()
    return course

@router.delete("/{course_id}")
def delete_course(request, course_id: int):
    dosen_or_admin_only(request)
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return {"success": True, "message": "Course deleted"}