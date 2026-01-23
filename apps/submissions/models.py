# =========================================================
# Deskripsi Program:
# Model Submission digunakan untuk merepresentasikan data
# pengumpulan tugas (submission) oleh mahasiswa.
#
# Model ini menyimpan informasi tugas yang dikumpulkan,
# identitas mahasiswa, file tugas, waktu terakhir diubah,
# serta nilai hasil penilaian.
# =========================================================

# Import modul models Django
from django.db import models

# Import model Assignment sebagai relasi ForeignKey
from apps.assignments.models import Assignment

# Import model Mahasiswa sebagai relasi ForeignKey
from apps.user.mahasiswa.models import Mahasiswa


class Submission(models.Model):
    """
    Model Submission merepresentasikan pengumpulan tugas
    oleh mahasiswa pada suatu assignment.
    """

    # Relasi ke model Assignment
    # Satu assignment dapat memiliki banyak submission
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE
    )

    # Relasi ke model Mahasiswa (pengumpul tugas)
    # Bersifat opsional (misalnya untuk data dummy atau arsip)
    student = models.ForeignKey(
        Mahasiswa,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Menyimpan waktu terakhir submission diperbarui
    # auto_now=True akan otomatis mengupdate timestamp
    lastModified = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    # File tugas yang diunggah oleh mahasiswa
    # Disimpan di folder "submissions/"
    file = models.FileField(
        upload_to="submissions/"
    )

    # Nilai hasil penilaian tugas
    # Bersifat opsional (diisi oleh dosen)
    grade = models.FloatField(
        null=True,
        blank=True
    )


    #Property digunakan untuk data turunan helper 
    @property
    def student_name(self):
        """
        Mengembalikan nama mahasiswa pengumpul tugas.

        Return:
        - Nama mahasiswa jika tersedia
        - 'Unknown' jika data mahasiswa kosong
        """
        return self.student.name if self.student else "Unknown"

    @property
    def file_url(self):
        """
        Mengembalikan URL file submission.

        Return:
        - URL file jika tersedia
        - String kosong jika file tidak ada
        """
        return self.file.url if self.file else ""

    @property
    def student_nim(self):
        """
        Mengembalikan NIM mahasiswa pengumpul tugas.

        Return:
        - NIM mahasiswa jika tersedia
        - '-' jika data mahasiswa kosong
        """
        return self.student.nim if self.student else "-"
