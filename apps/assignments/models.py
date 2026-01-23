# =========================================================
# Deskripsi Program:
# Model Assignment digunakan untuk merepresentasikan data
# tugas (assignment) dalam sistem pembelajaran.
#
# Setiap assignment terhubung dengan satu Lesson
# dan memiliki informasi judul, deskripsi, serta batas waktu.
# =========================================================

# Import modul models Django untuk definisi database
from django.db import models

# Import model Lesson sebagai relasi ForeignKey
from apps.lessons.models import Lesson


class Assignment(models.Model):
    """
    Model Assignment merepresentasikan tugas yang diberikan
    pada suatu lesson/mata pelajaran.
    """

    # Relasi ke model Lesson (satu lesson dapat memiliki banyak assignment)
    lesson = models.ForeignKey(
        Lesson,
        related_name="assignments",
        on_delete=models.CASCADE
    )

    # Judul tugas (opsional)
    title = models.TextField(
        null=True,
        blank=True
    )

    # Deskripsi atau penjelasan tugas (opsional)
    description = models.TextField(
        null=True,
        blank=True
    )

    # Batas waktu pengumpulan tugas
    deadline = models.DateTimeField()

    def __str__(self):
        """
        Representasi string dari objek Assignment.
        Digunakan pada Django Admin dan shell.
        Agar ketika ada model yang berelasi dengan model assignment yang menggunakan fitu select option dapat menampilkan nama judul dari assignmentnya
        """
        return self.title if self.title else "Assignment Tanpa Judul"
