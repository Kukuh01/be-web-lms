from ninja import Router, Schema, File
from ninja.files import UploadedFile
from .models import Submission
from core.jwt_auth import JWTAuth

router = Router(auth=JWTAuth(), tags=["Submission"])

@router.post("/")
def submit_assignment(
    request,
    assignment_id: int,
    student_id: int,
    file: UploadedFile = File(...)
):
    submission = Submission.objects.create(
        assignment_id=assignment_id,
        student_id=student_id,
        file=file
    )
    return {"id": submission.id}
