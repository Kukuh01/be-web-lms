from ninja import Router, Schema, Form, File
from ninja.files import UploadedFile
from .models import Course
from core.jwt_auth import JWTAuth
from apps.lessons.api import LessonOut
from core.permissions import dosen_only
from typing import Optional, List

router = Router(tags=["Courses"])
# router = Router(auth=JWTAuth(), tags=["Courses"])

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
    description: str
    instructor: InstructorOut
    thumbnail: Optional[str] = None

class CourseDetail(CourseOut):
    lessons: List[LessonOut]

@router.post("/", response=CourseOut)
def create_course(
    request,
    title: str = Form(...),
    description: str = Form(...),
    instructor_id: int = Form(...),
    thumbnail: UploadedFile = File(None),
):
    dosen_only(request)

    course = Course.objects.create(
        title=title,
        description=description,
        instructor_id=instructor_id,
        thumbnail=thumbnail
    )
    
    return course

@router.get("/", response=List[CourseOut])
def list_courses(request):
    return Course.objects.all()

@router.get("/{course_id}", response=CourseDetail)
def get_course(request, course_id: int):
    return Course.objects.prefetch_related("lessons").get(id=course_id)