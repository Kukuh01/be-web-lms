from django.db import models
from apps.courses.models import Course

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title if self.title else "Assignment Tanpa Judul"