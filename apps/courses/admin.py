# =========================================================
# Deskripsi Program:
# Konfigurasi Django Admin untuk model Course.
#
# Kelas CourseAdmin digunakan untuk mengatur tampilan,
# pencarian, filter, dan representasi data Course
# pada Django Admin Panel.
# =========================================================

# Import modul admin Django
from django.contrib import admin

# Import model Course
from .models import Course


# Mendaftarkan model Course ke Django Admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Kelas CourseAdmin digunakan untuk mengelola tampilan
    dan perilaku model Course di Django Admin.
    """

    # Field yang ditampilkan pada halaman daftar course
    list_display = (
        "title",     # Judul course
        "instructor", # Nama dosen pengampu course
    )

    # Field yang dapat digunakan untuk pencarian
    # instructor__name menggunakan relasi ForeignKey
    search_fields = (
        "title",
        "instructor__name",
    )

    # Filter yang tersedia di sidebar admin
    list_filter = (
        "instructor",
    )

    # Mengaktifkan fitur autocomplete untuk field instructor
    autocomplete_fields = (
        "instructor",
    )

    #  Old Function to get instructor name without hardcode in model dosen
    # def get_dosen(self, obj):
    #     """
    #     Method untuk menampilkan nama dosen pengampu
    #     pada kolom list_display.

    #     Parameter:
    #     - obj : instance Course

    #     Return:
    #     - Nama dosen (string)
    #     """
    #     return obj.instructor.name

    # # Mengubah judul kolom di admin menjadi "Dosen"
    # get_dosen.short_description = "Dosen"