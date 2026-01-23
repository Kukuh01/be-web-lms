from ninja import Router, Schema
from .models import Assignment
from datetime import datetime
from typing import List
from core.jwt_auth import JWTAuth
from core.permissions import dosen_or_admin_only
from .services import AssignmentService
from .schemas import AssignmentOut, AssignmentIn

router = Router(auth=JWTAuth(), tags=["Assignment"])
service = AssignmentService()

@router.get("/{lesson_id}", response=List[AssignmentOut])
def list_assignments(request, lesson_id: int):
    return service.list_by_lesson(lesson_id)

@router.post(
    "/lessons/{lesson_id}/assignments",
    response={201: AssignmentOut}
)
def create_assignment(request, lesson_id: int, payload: AssignmentIn):
    dosen_or_admin_only(request)
    assignment = service.create(lesson_id, payload)
    return 201, assignment

@router.put(
    "/assignments/{assignment_id}",
    response=AssignmentOut
)
def update_assignment(request, assignment_id: int, payload: AssignmentIn):
    dosen_or_admin_only(request)
    return service.update(assignment_id, payload)

@router.delete(
    "/assignments/{assignment_id}",
    response={204: None}
)
def delete_assignment(request, assignment_id: int):
    dosen_or_admin_only(request)
    service.delete(assignment_id)
    return 200, {
        "success": True,
        "message": "Assignment berhasil dihapus"
    }