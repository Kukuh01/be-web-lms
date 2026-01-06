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