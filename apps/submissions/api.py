from ninja import Router, File, Form
from ninja.files import UploadedFile

# Auth & Permissions
from core.jwt_auth import JWTAuth
from core.permissions import dosen_or_admin_only, mahasiswa_only
from .schemas import SubmissionResponse, GradeIn, ErrorSchema
from .services import SubmissionsService

router = Router(auth=JWTAuth(), tags=["Submissions"])
submission_service = SubmissionsService()

@router.post("/", response={201: SubmissionResponse})
def submit_submission(
    request,
    assignment_id: int = Form(...),
    file_data: UploadedFile = File(...)
):
    mahasiswa_only(request)
    submission = submission_service.submit_submission(
        user=request.auth,
        assignment_id=assignment_id,
        file_data=file_data
    )
    return 201, submission

@router.get(
    "/assignment/{assignment_id}",
    response={200: SubmissionResponse, 404: ErrorSchema}
)
def get_latest_submission(request, assignment_id: int):
    submission = submission_service.get_latest_submission(
        request.auth, assignment_id
    )
    return 200, submission

@router.post("/{submission_id}/grade", response={200: SubmissionResponse})
def grade_submission(request, submission_id: int, data: GradeIn):
    dosen_or_admin_only(request)
    submission = submission_service.grade_submission(
        submission_id, data.grade
    )
    return 200, submission