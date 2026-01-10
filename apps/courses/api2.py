from ninja import Router, Schema, Form, File
from ninja.files import UploadedFile
from typing import Optional, List
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

# Import Models
from .models import Course
from apps.lessons.models import Lesson
from apps.assignments.models import Assignment
from apps.submissions.models import Submission
from datetime import datetime

# Auth & Permissions
from core.jwt_auth import JWTAuth
from core.permissions import dosen_only, dosen_or_admin_only

router = Router(auth=JWTAuth(), tags=["Courses Management"])

# ==========================================
# 1. SCHEMAS (Hierarki Data)
# ==========================================

# --- Submission Schema ---
class SubmissionOut(Schema):
    id: int
    student_name: str
    student_nim: str
    submitted_at: Optional[str] = None # datetime
    file_url: str
    grade: Optional[float]
    feedback: Optional[str]

    @staticmethod
    def resolve_student_name(obj):
        return obj.student.name if obj.student else "Unknown"

    @staticmethod
    def resolve_student_nim(obj):
        return obj.student.nim if obj.student else "-"
    
    @staticmethod
    def resolve_submitted_at(obj):
        return obj.lastModified

    @staticmethod
    def resolve_file_url(obj):
        return obj.file.url if obj.file else ""

# --- Assignment Schema ---
class AssignmentIn(Schema):
    title: str
    description: Optional[str] = None
    deadline: datetime # ISO Datetime string

class AssignmentOut(AssignmentIn):
    id: int
    submissions: List[SubmissionOut] = []

# --- Lesson Schema ---
class LessonIn(Schema):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None

class LessonOut(LessonIn):
    id: int
    # Assignment opsional (karena lesson mungkin belum punya tugas)
    assignment: Optional[AssignmentOut] = None 

    @staticmethod
    def resolve_assignment(obj):
        # Mengambil assignment pertama (Logic 1 Lesson = 1 Assignment)
        return obj.assignment_set.first()

# --- Course Schema ---
class InstructorOut(Schema):
    id: int
    name: str

class CourseIn(Schema):
    # Schema ini dipakai jika input via JSON (bukan Form)
    # Tapi create_course di bawah pakai Form(...) jadi ini opsional
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

class CourseDetail(CourseOut):
    lessons: List[LessonOut]

# ==========================================
# 2. CONTROLLERS
# ==========================================

# --- COURSE ENDPOINTS ---

@router.get("/", response=List[CourseOut])
def list_courses(request):
    # Optimization: Select related untuk instructor agar tidak N+1 Query
    return Course.objects.select_related("instructor").all()

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

# --- LESSON ENDPOINTS ---

@router.post("/{course_id}/lessons", response=LessonOut)
def create_lesson(request, course_id: int, payload: LessonIn):
    dosen_or_admin_only(request)
    course = get_object_or_404(Course, id=course_id)
    lesson = Lesson.objects.create(course=course, **payload.dict())
    return lesson

@router.put("/lessons/{lesson_id}", response=LessonOut)
def update_lesson(request, lesson_id: int, payload: LessonIn):
    dosen_or_admin_only(request)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    for attr, value in payload.dict().items():
        setattr(lesson, attr, value)
    lesson.save()
    return lesson

@router.delete("/lessons/{lesson_id}")
def delete_lesson(request, lesson_id: int):
    dosen_or_admin_only(request)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.delete()
    return {"success": True}

# --- ASSIGNMENT ENDPOINTS ---

@router.post("/lessons/{lesson_id}/assignment")
def create_or_update_assignment(request, lesson_id: int, payload: AssignmentIn):
    dosen_or_admin_only(request)
    # Logic: 1 Lesson hanya boleh punya 1 Assignment
    # Kita gunakan update_or_create berdasarkan lesson_id
    assignment, created = Assignment.objects.update_or_create(
        lesson_id=lesson_id,
        defaults=payload.dict()
    )
    return {"success": True, "id": assignment.id, "created": created}

@router.delete("/lessons/{lesson_id}/assignment")
def delete_assignment(request, lesson_id: int):
    dosen_or_admin_only(request)
    # Hapus semua assignment di lesson ini (seharusnya cuma 1)
    Assignment.objects.filter(lesson_id=lesson_id).delete()
    return {"success": True}

# --- GRADING ENDPOINT ---

@router.post("/submissions/{submission_id}/grade")
def grade_submission(request, submission_id: int, grade: float, feedback: str = None):
    dosen_or_admin_only(request)
    submission = get_object_or_404(Submission, id=submission_id)
    submission.grade = grade
    submission.feedback = feedback
    submission.save()
    return {"success": True}