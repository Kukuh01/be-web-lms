from django.core.management.base import BaseCommand
from apps.assignments.models import Assignment
from apps.lessons.models import Lesson
from django.utils import timezone

class Command(BaseCommand):
    help = "Seed assignments"

    def handle(self, *args, **kwargs):
        lessons = Lesson.objects.all()

        for lesson in lessons:
            Assignment.objects.get_or_create(
                lesson=lesson,
                title=f"Tugas - {lesson.title}",
                defaults={
                    "description": "Kerjakan tugas berikut",
                    "deadline": timezone.now(),
                }
            )

        self.stdout.write(self.style.SUCCESS("Assignments seeded"))
