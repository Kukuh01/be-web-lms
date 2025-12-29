from django.core.management.base import BaseCommand
from apps.courses.models import Course
from apps.user.dosen.models import Dosen 

class Command(BaseCommand):
    help = "Seed courses"

    def handle(self, *args, **kwargs):
        instructor = Dosen.objects.filter(user__username="dosen1").first()

        if not instructor:
            self.stdout.write(self.style.ERROR("Instructor (Dosen) belum ada"))
            return

        courses = [
            "Pemrograman Python",
            "Basis Data",
            "Web Development",
        ]

        for title in courses:
            Course.objects.get_or_create(
                title=title,
                defaults={
                    "description": f"Course {title}",
                    "instructor": instructor,  # ✅ BENAR: Dosen instance
                }
            )

        self.stdout.write(self.style.SUCCESS("Courses seeded ✅"))
