from django.db import models
from apps.user.dosen.models import Dosen

class Course(models.Model):
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    linkMeet = models.TextField(null=True, blank=True)
    linkWa = models.TextField(null=True, blank=True)
    instructor = models.ForeignKey(
        Dosen,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title