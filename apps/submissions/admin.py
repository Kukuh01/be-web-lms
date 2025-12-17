from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'grade')
    list_filter = ('assignment',)
    search_fields = ('student__username',)