from django.db import models
from apps.lessons.models import Lesson

class Assignment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title if self.title else "Assignment Tanpa Judul"