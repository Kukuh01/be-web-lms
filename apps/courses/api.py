# apps/courses/api.py (Versi Updated)
from ninja import Router, Form, File
from ninja.files import UploadedFile
from typing import Optional, List

# Import Service
from .services import CourseService

from core.jwt_auth import JWTAuth
from core.permissions import dosen_only, dosen_or_admin_only
from .schemas import CourseIn, CourseOut, CourseDetail, CourseStatsOut

router = Router(auth=JWTAuth(), tags=["Courses Management"])
course_service = CourseService() 

@router.get("/stats", response=CourseStatsOut)
def get_course_stats(request):
    """
    Mengambil jumlah total kursus.
    Data di-cache di Redis agar tidak membebani DB (Count Query).
    """
    return course_service.get_course_stats()

@router.get("/", response=List[CourseOut])
def list_courses(request):
    return course_service.get_all_courses()

@router.get("/{course_id}", response=CourseDetail)
def get_course(request, course_id: int):
    return course_service.get_course_by_id(course_id)

@router.post("/", response={201: CourseOut})
def create_course(
    request,
    data: CourseIn = Form(...),
    thumbnail: UploadedFile = File(None),
):
    dosen_only(request)
    course = course_service.create_course(
        thumbnail=thumbnail,
        **data.dict()
    )
    return 201, course

@router.put("/{course_id}", response={200: CourseOut})
def update_course(
    request,
    course_id: int,
    data: CourseIn = Form(...),
    thumbnail: UploadedFile = File(None),
):
    dosen_or_admin_only(request)
    course = course_service.update_course(
        course_id,
        thumbnail,
        **data.dict()
    )
    return 200, course

@router.delete("/{course_id}")
def delete_course(request, course_id: int):
    dosen_or_admin_only(request)
    course_service.delete_course(course_id)
    return 200, {
        "success": True,
        "message": "Course berhasil dihapus"
    }