from django.db import models
from apps.courses.models import Course

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title