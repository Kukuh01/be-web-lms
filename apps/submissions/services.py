from .models import Submission, Assignment
from apps.user.mahasiswa.models import Mahasiswa
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404

class SubmissionsService:
    def submit_submission(self, user, assignment_id: int, file_data):
        mahasiswa = Mahasiswa.objects.filter(user=user).first()
        if not mahasiswa:
            raise HttpError(403, "Hanya mahasiswa yang boleh mengumpulkan tugas.")
        
        assignment = get_object_or_404(Assignment, id=assignment_id)

        submission = Submission.objects.create(
            assignment=assignment,
            student=mahasiswa,
            file=file_data
        )

        return submission

    def get_latest_submission(self, user, assignment_id: int):
        assignment = get_object_or_404(Assignment, id=assignment_id)
        mahasiswa = Mahasiswa.objects.filter(user=user).first()
        if not mahasiswa:
            raise HttpError(403, "Hanya mahasiswa yang boleh mengumpulkan tugas.")

        submission = Submission.objects.filter(
            assignment_id=assignment,
            student=mahasiswa
        ).order_by("-lastModified").first()

        if not submission:
            raise HttpError(404, "Belum ada pengumpulan tugas")

        return submission

    def grade_submission(self, submission_id: int, grade: float):
        submission = get_object_or_404(Submission, id=submission_id)
        submission.grade = grade
        submission.save()
        return submission