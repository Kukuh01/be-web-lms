# =========================================================
# Deskripsi Program:
# Konfigurasi tampilan dan pengelolaan model User kustom
# pada Django Admin Panel.
#
# File ini bertujuan untuk:
# - Mendaftarkan model User ke Django Admin
# - Menyesuaikan tampilan data user
# - Menambahkan field "role" ke form admin
# =========================================================

# Import modul admin Django
from django.contrib import admin

# Import UserAdmin bawaan Django untuk kustomisasi admin user
from django.contrib.auth.admin import UserAdmin

# Import model User kustom
from .models import User


# Mendaftarkan model User ke Django Admin menggunakan decorator
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Kelas CustomUserAdmin digunakan untuk mengatur
    tampilan dan perilaku model User di Django Admin.
    """

    # Menentukan model yang digunakan
    model = User

    # Field yang ditampilkan pada halaman daftar user
    list_display = (
        'username',   # Username user
        'email',      # Email user
        'role',       # Peran user (admin/dosen/mahasiswa)
        'is_staff',   # Status staff
        'is_active',  # Status aktif user
    )

    # Filter yang tersedia di sidebar admin
    list_filter = ('role', 'is_staff', 'is_active')

    # Field yang bisa digunakan untuk pencarian
    search_fields = ('username', 'email')

    # Menambahkan field "role" ke halaman detail/edit user
    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )
