from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.user.dosen.models import Dosen

User = get_user_model()

class Command(BaseCommand):
    help = "Seed data dosen"

    def handle(self, *args, **kwargs):
        dosen_data = [
            {
                "username": "dosen1",
                "email": "dosen1@kampus.ac.id",
                "password": "password123",
                "name": "Dr. Andi Wijaya",
                "nidn": "1234567890",
                "fakultas": "Fakultas Ilmu Komputer",
            },
            {
                "username": "dosen2",
                "email": "dosen2@kampus.ac.id",
                "password": "password123",
                "name": "Dr. Budi Santoso",
                "nidn": "0987654321",
                "fakultas": "Fakultas Teknik",
            },
        ]

        for data in dosen_data:
            user, user_created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                    "role": "dosen",
                }
            )

            if user_created:
                user.set_password(data["password"])
                user.save()
                self.stdout.write(f"User {user.username} dibuat")

            dosen, dosen_created = Dosen.objects.get_or_create(
                user=user,
                defaults={
                    "name": data["name"],
                    "nidn": data["nidn"],
                    "fakultas": data["fakultas"],
                }
            )

            if dosen_created:
                self.stdout.write(f"Dosen {dosen.name} dibuat")

        self.stdout.write(self.style.SUCCESS("Seeder dosen selesai ✅"))
