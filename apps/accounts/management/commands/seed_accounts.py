from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Seed users (admin, dosen, mahasiswa)"

    def handle(self, *args, **kwargs):
        users = [
            {
                "username": "admin",
                "email": "admin@lms.com",
                "password": "admin123",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "username": "dosen1",
                "email": "dosen1@kampus.ac.id",
                "password": "password123",
                "role": "dosen",
            },
            {
                "username": "dosen2",
                "email": "dosen2@kampus.ac.id",
                "password": "password123",
                "role": "dosen",
            },
            {
                "username": "mahasiswa1",
                "email": "mahasiswa1@kampus.ac.id",
                "password": "password123",
                "role": "mahasiswa",
            },
            {
                "username": "mahasiswa2",
                "email": "mahasiswa2@kampus.ac.id",
                "password": "password123",
                "role": "mahasiswa",
            },
        ]

        for user_data in users:
            user, created = User.objects.get_or_create(
                username=user_data["username"],
                defaults=user_data,
            )

            if created:
                user.set_password(user_data["password"])
                user.save()
                self.stdout.write(f"User {user.username} dibuat")

        self.stdout.write(self.style.SUCCESS("Users seeded"))
