from ninja import Router, Schema
from .models import Course
from core.jwt_auth import JWTAuth

router = Router(auth=JWTAuth(), tags=["Courses"])

class CourseIn(Schema):
    title: str
    description: str
    instructor_id: int

class CourseOut(Schema):
    id: int
    title: str
    description: str
    instructor_id: int

@router.post("/")
def create_course(request, data: CourseIn):
    course = Course.objects.create(
        title=data.title,
        description=data.description,
        instructor_id=data.instructor_id
    )
    return {"id": course.id}

@router.get("/", response=list[CourseOut])
def list_courses(request):
    return Course.objects.all()