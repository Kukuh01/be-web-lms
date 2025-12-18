from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "get_dosen")
    search_fields = ("title", 'instructor__name')
    list_filter = ("instructor",)
    autocomplete_fields = ('instructor',)

    def get_dosen(self, obj):
        return obj.instructor.name
    
    get_dosen.short_description = 'Dosen'