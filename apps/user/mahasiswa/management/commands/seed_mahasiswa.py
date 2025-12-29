from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.user.mahasiswa.models import Mahasiswa

User = get_user_model()

class Command(BaseCommand):
    help = "Seed data mahassiwa"

    def handle(self, *args, **kwargs):
        mahasiswa_data = [
            {
                "username": "mahasiswa1",
                "email": "mahasiswa1@kampus.ac.id",
                "password": "password123",
                "name": "Silvanus Kukuh Prasetyo",
                "nim": "A11.2023.14963",
                "program_studi": "Teknik Informatika",
                "angkatan": 2022,
            },
            {
                "username": "mahasiswa2",
                "email": "mahasiswa2@kampus.ac.id",
                "password": "password123",
                "name": "Calvin Samuel Simbolon",
                "nim": "A11.2023.14880",
                "program_studi": "Teknik Informatika",
                "angkatan": 2022,
            },
        ]

        for data in mahasiswa_data:
            user, user_created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                    "role": "mahasiswa",
                }
            )

            if user_created:
                user.set_password(data["password"])
                user.save()
                self.stdout.write(f"User {user.username} dibuat")

            mahasiswa, mahasiswa_created = Mahasiswa.objects.get_or_create(
                user=user,
                defaults={
                    "name": data["name"],
                    "nim": data["nim"],
                    "program_studi": data["program_studi"],
                    "angkatan": data["angkatan"],
                }
            )

            if mahasiswa_created:
                self.stdout.write(f"Mahasiswa {mahasiswa.name} dibuat")

        self.stdout.write(self.style.SUCCESS("Seeder Mahasiswa selesai ✅"))
