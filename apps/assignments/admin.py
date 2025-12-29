from django.contrib import admin
from .models import Assignment

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'title','deadline')
    list_filter = ('lesson',)