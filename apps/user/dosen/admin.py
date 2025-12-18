from django.contrib import admin
from .models import Dosen

@admin.register(Dosen)
class DosenAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "nidn", "fakultas")
    search_fields = ("name","user__username","nidn", "fakultas")
    list_filter = ("fakultas",)