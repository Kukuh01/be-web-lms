from django.contrib import admin
from .models import Mahasiswa

@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "nim", "program_studi", "angkatan")
    search_fields = ("name","user","user__username","nim", "program_studi", "angkatan")
    list_filter = ("angkatan","program_studi")