from ninja import Router, File, Form, Schema
from ninja.files import UploadedFile
from typing import Optional
from datetime import datetime
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError

# Models
from .models import Submission, Assignment
from apps.user.mahasiswa.models import Mahasiswa

# Auth & Permissions
from core.jwt_auth import JWTAuth
from core.permissions import dosen_or_admin_only

router = Router(auth=JWTAuth(), tags=["Submissions"])

# --- SCHEMAS ---

class SubmissionResponse(Schema):
    id: int
    file_url: str
    lastModified: Optional[datetime] = None
    grade: Optional[float] = None # Ubah ke float agar konsisten
    student_name: str

class ErrorSchema(Schema):
    detail: str

class GradeIn(Schema):
    grade: float

# --- ENDPOINTS ---

@router.post("/", response=SubmissionResponse)
def submit_assignment(
    request,
    assignment_id: int = Form(...),
    file: UploadedFile = File(...)
):
    user = request.auth

    try:
        mahasiswa = Mahasiswa.objects.get(user=user)
    except Mahasiswa.DoesNotExist:
        raise HttpError(403, "Hanya mahasiswa yang boleh mengumpulkan tugas.")

    assignment = get_object_or_404(Assignment, id=assignment_id)

    submission = Submission.objects.create(
        assignment=assignment,
        student=mahasiswa,
        file=file
    )

    return submission

@router.get(
    "/assignment/{assignment_id}",
    response={200: SubmissionResponse, 404: ErrorSchema}
)
def get_latest_submission(request, assignment_id: int):
    user = request.auth
    
    try:
        mahasiswa = Mahasiswa.objects.get(user=user)
    except Mahasiswa.DoesNotExist:
        return 404, {"detail": "Profile mahasiswa tidak ditemukan"}

    # 2. Ambil submission terakhir
    submission = Submission.objects.filter(
        assignment_id=assignment_id,
        student=mahasiswa
    ).order_by('-lastModified').first()

    if not submission:
        return 404, {"detail": "Belum ada pengumpulan tugas"}

    return submission

@router.post("/{submission_id}/grade", response={200: dict})
def grade_submission(request, submission_id: int, data: GradeIn):
    dosen_or_admin_only(request)
    
    submission = get_object_or_404(Submission, id=submission_id)
    
    # Simpan nilai DAN feedback
    submission.grade = data.grade
    submission.save()
    
    return {"success": True, "message": "Nilai berhasil disimpan"}