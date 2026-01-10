from ninja import Router, Schema
from .models import Assignment
from datetime import datetime
from typing import List
from core.jwt_auth import JWTAuth
from core.permissions import dosen_or_admin_only
from apps.submissions.api import SubmissionResponse

router = Router(auth=JWTAuth(), tags=["Assignment"])

class AssignmentIn(Schema):
    # HAPUS lesson_id dari sini karena sudah ada di URL
    title: str
    description: str
    deadline: datetime

class AssignmentOut(Schema):
    id: int
    lesson_id: int
    title: str
    description: str
    deadline: datetime
    submissions: List[SubmissionResponse] = [] 

    @staticmethod
    def resolve_submissions(obj):
        # Mengambil semua submission terkait assignment ini
        return obj.submission_set.all()

@router.get("/{lesson_id}", response=List[AssignmentOut])
def list_assignments(request, lesson_id: int):
    return Assignment.objects.filter(lesson_id=lesson_id)

@router.post("/{lesson_id}/assignment")
def create_or_update_assignment(request, lesson_id: int, payload: AssignmentIn):
    dosen_or_admin_only(request)
    
    # Payload sekarang hanya berisi: title, description, deadline
    # lesson_id diambil dari parameter URL function
    
    assignment, created = Assignment.objects.update_or_create(
        lesson_id=lesson_id,  # Lookup berdasarkan ID dari URL
        defaults=payload.dict() # Update field lainnya dari Body
    )
    return {"success": True, "id": assignment.id, "created": created}

@router.delete("/{lesson_id}/assignment")
def delete_assignment(request, lesson_id: int):
    dosen_or_admin_only(request)
    Assignment.objects.filter(lesson_id=lesson_id).delete()
    return {"success": True}