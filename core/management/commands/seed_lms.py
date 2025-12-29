from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Seed all LMS data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding Account...")
        call_command("seed_accounts")

        self.stdout.write("Seeding Mahasiswa...")
        call_command("seed_mahasiswa")

        self.stdout.write("Seeding Dosen...")
        call_command("seed_dosen")

        self.stdout.write("Seeding courses...")
        call_command("seed_courses")

        self.stdout.write("Seeding lessons...")
        call_command("seed_lessons")

        self.stdout.write("Seeding assignments...")
        call_command("seed_assignments")

        self.stdout.write(self.style.SUCCESS("Semua data LMS berhasil di-seed"))
