# =========================================================
# Deskripsi Program:
# Model User kustom yang mewarisi AbstractUser Django.
#
# Model ini digunakan untuk menambahkan atribut "role"
# pada user guna mendukung sistem otorisasi berbasis peran
# (Role-Based Access Control / RBAC).
#
# Role yang didukung:
# - admin
# - dosen
# - mahasiswa
# =========================================================

# Import AbstractUser untuk membuat model user kustom
from django.contrib.auth.models import AbstractUser

# Import modul models untuk definisi database
from django.db import models


class User(AbstractUser):
    """
    Model User kustom yang memperluas AbstractUser Django.

    Model ini menambahkan field 'role' untuk menentukan
    peran user dalam sistem.
    """

    class Role(models.TextChoices):
        """
        Enum Role untuk mendefinisikan pilihan peran user.
        Digunakan agar nilai role konsisten dan terkontrol.
        """
        ADMIN = "admin"
        DOSEN = "dosen"
        Mahasiswa = "mahasiswa"

    # Field role untuk menyimpan peran user
    role = models.CharField(
        max_length=20,          # Panjang maksimal karakter
        choices=Role.choices,   # Pilihan nilai role
    )
