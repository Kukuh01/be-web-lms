from django.core.management.base import BaseCommand
from apps.lessons.models import Lesson
from apps.courses.models import Course

class Command(BaseCommand):
    help = "Seed lessons"

    def handle(self, *args, **kwargs):
        courses = Course.objects.all()

        for course in courses:
            for i in range(1, 4):
                Lesson.objects.get_or_create(
                    course=course,
                    title=f"Lesson {i} - {course.title}",
                    defaults={
                        "content": "Materi pembelajaran",
                    }
                )

        self.stdout.write(self.style.SUCCESS("Lessons seeded"))