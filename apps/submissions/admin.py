from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'get_mahasiswa', 'grade')
    list_filter = ('assignment',)
    search_fields = ('student__username', 'student__first_name') 
    autocomplete_fields = ('student',)

    @admin.display(description='Mahasiswa', ordering='student__name')
    def get_mahasiswa(self, obj):
        if obj.student:
            return obj.student.name if hasattr(obj.student, 'name') else obj.student.username
        return "-"