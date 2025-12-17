from ninja import Router, Schema
from .models import Assignment

router = Router()

class AssignmentIn(Schema):
    course_id: int
    deadline: str

@router.post("/")
def create_assignment(request, data: AssignmentIn):
    assignment = Assignment.objects.create(**data.dict())
    return {"id": assignment.id}

@router.get("/course/{course_id}")
def list_assignments(request, course_id: int):
    return Assignment.objects.filter(course_id=course_id)