# apps/courses/api.py (Versi Updated)
from ninja import Router, Schema, Form, File
from ninja.files import UploadedFile
from typing import Optional, List

# Import Service
from .services import CourseService

from core.jwt_auth import JWTAuth
from core.permissions import dosen_only, dosen_or_admin_only
from apps.lessons.api import LessonOut

router = Router(auth=JWTAuth(), tags=["Courses Management"])
service = CourseService() # Inisialisasi Service

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

# --- COURSE ENDPOINTS ---

@router.get("/", response=List[CourseOut])
def list_courses(request):
    # Logic pindah ke service. Service me-return List of Course Objects.
    # Ninja akan otomatis mengubah Objects ini menjadi JSON sesuai Schema CourseOut.
    return service.get_all_courses()

@router.get("/{course_id}", response=CourseDetail)
def get_course(request, course_id: int):
    return service.get_course_by_id(course_id)

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
    # Bungkus data dalam dictionary agar rapi saat dikirim ke service
    payload = {
        "title": title,
        "description": description,
        "instructor_id": instructor_id,
        "linkMeet": linkMeet,
        "linkWa": linkWa,
        "thumbnail": thumbnail
    }
    return service.create_course(**payload)

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
    
    # Pisahkan data text dan file
    payload = {
        "title": title,
        "description": description,
        "instructor_id": instructor_id,
        "linkMeet": linkMeet,
        "linkWa": linkWa,
    }
    
    return service.update_course(course_id, file_data=thumbnail, **payload)

@router.delete("/{course_id}")
def delete_course(request, course_id: int):
    dosen_or_admin_only(request)
    service.delete_course(course_id)
    return {"success": True, "message": "Course deleted"}