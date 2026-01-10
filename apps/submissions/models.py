from django.db import models
from apps.assignments.models import Assignment
from apps.user.mahasiswa.models import Mahasiswa

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Mahasiswa,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    lastModified = models.DateTimeField(auto_now=True, null=True, blank=True)
    file = models.FileField(upload_to="submissions/")
    grade = models.FloatField(null=True, blank=True)

    @property
    def student_name(self):
        return self.student.name if self.student else "Unknown"

    @property
    def file_url(self):
        return self.file.url if self.file else ""
    
    @property
    def student_nim(self):
        return self.student.nim if self.student else "-"