from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "instructor")
    search_fields = ("title",)
    list_filter = ("instructor",)