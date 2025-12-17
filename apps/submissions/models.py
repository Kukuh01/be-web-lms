from django.db import models
from apps.assignments.models import Assignment
from apps.accounts.models import User

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "mahasiswa"}
    )
    file = models.FileField(upload_to="submissions/")
    grade = models.FloatField(null=True, blank=True)