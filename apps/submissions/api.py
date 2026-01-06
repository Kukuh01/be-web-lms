from ninja import Router, File, Form, Schema
from ninja.files import UploadedFile
from typing import Optional
from datetime import datetime
from .models import Submission
from apps.user.mahasiswa.models import Mahasiswa
from core.jwt_auth import JWTAuth # Pastikan ini sudah benar

router = Router(auth=JWTAuth(), tags=["Submission"])

class SubmissionResponse(Schema):
    id: int
    file_url: str
    lastModified: Optional[datetime] = None
    grade: Optional[str] = None
    student_name: str

class ErrorSchema(Schema):
    detail: str

@router.post("/", response=SubmissionResponse)
def submit_assignment(
    request,
    assignment_id: int = Form(...),
    file: UploadedFile = File(...)
):
    user = request.auth

    mahasiswa = Mahasiswa.objects.get(user=user)

    submission = Submission.objects.create(
        assignment_id=assignment_id,
        student=mahasiswa,
        file=file
    )

    return {
        "id": submission.id,
        "file_url": submission.file.url,
        "lastModified": submission.lastModified,
        "grade": submission.grade,
        "student_name": mahasiswa.user.username
    }

@router.get(
    "/assignment/{assignment_id}",
    response={
        200: SubmissionResponse,
        404: ErrorSchema
    }
)
def get_latest_submission(request, assignment_id: int):
    user = request.auth
    mahasiswa = Mahasiswa.objects.get(user=user)

    submission = Submission.objects.filter(
        assignment_id=assignment_id,
        student=mahasiswa
    ).last()

    if not submission:
        return 404, {"detail": "Belum ada pengumpulan"}

    return {
        "id": submission.id,
        "file_url": submission.file.url,
        "grade": submission.grade,
        "lastModified": submission.lastModified,
        "student_name": mahasiswa.name
    }