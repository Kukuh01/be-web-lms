from django.db import models
from apps.user.dosen.models import Dosen

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(
        Dosen,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title