# apps/lessons/services.py
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .models import Course, Lesson

class LessonService:
    # Key Pattern: lessons:course:{course_id}
    CACHE_KEY_LIST = "lessons:course:{}" 
    TIMEOUT = 60 * 15  # 15 Menit

    def get_lessons_by_course(self, course_id: int):
        # 1. Definisi Key Cache
        key = self.CACHE_KEY_LIST.format(course_id)

        # 2. Cek Redis
        cached_data = cache.get(key)
        if cached_data:
            return cached_data

        # 3. Query DB (Logic Lama Anda)
        # Kita fetch Course dulu dengan prefetch yang lengkap
        course = get_object_or_404(
            Course.objects.prefetch_related(
                "lessons",
                "lessons__assignments_set", 
                "lessons__assignments_set__submission_set", 
                "lessons__assignments_set__submission_set__student" 
            ), 
            id=course_id
        )

        lessons = list(course.lessons.all())
        cache.set(key, lessons, self.TIMEOUT)
        
        return lessons

    def create_lesson(self, course_id: int, data: dict):
        course = get_object_or_404(Course, id=course_id)
        lesson = Lesson.objects.create(course=course, **data)
        
        cache.delete(self.CACHE_KEY_LIST.format(course_id))
        
        return lesson

    def update_lesson(self, lesson_id: int, data: dict):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        
        for attr, value in data.items():
            setattr(lesson, attr, value)
        lesson.save()

        cache.delete(self.CACHE_KEY_LIST.format(lesson.course_id))
        
        return lesson

    def delete_lesson(self, lesson_id: int):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        course_id = lesson.course_id
        
        lesson.delete()

        cache.delete(self.CACHE_KEY_LIST.format(course_id))
        
        return True