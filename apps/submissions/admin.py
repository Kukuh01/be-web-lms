from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'get_mahasiswa', 'grade')
    list_filter = ('assignment',)
    search_fields = ('student__name',)
    autocomplete_fields = ('student',)

    def get_mahasiswa(self, obj):
        return obj.student.name
    
    get_mahasiswa.short_description = 'Mahasiswa'