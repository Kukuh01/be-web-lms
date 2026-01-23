# apps/courses/services.py
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .models import Course

class CourseService:
    # Definisi Key Cache
    KEY_LIST = "courses:all"
    KEY_DETAIL = "course:{}"
    KEY_STATS = "course:stats"
    TIMEOUT = 60 * 60 

    def get_course_stats(self):
        # 1. Cek Redis
        stats = cache.get(self.KEY_STATS)
        if stats:
            return stats

        # 2. Hitung dari DB (Count Query)
        total = Course.objects.count()
        
        # Bisa ditambahkan stats lain jika perlu, misal per instruktur
        data = {
            "total_courses": total
        }

        # 3. Simpan ke Redis
        cache.set(self.KEY_STATS, data, self.TIMEOUT)
        
        return data

    def get_all_courses(self):
        # 1. Cek Redis
        cached_data = cache.get(self.KEY_LIST)
        if cached_data:
            return cached_data

        # 2. Query DB (Berat)
        # Kita gunakan logic query yang sama persis dengan api.py Anda
        queryset = Course.objects.select_related("instructor")\
            .prefetch_related(
                "lessons", 
                "lessons__assignment_set",
                "lessons__assignment_set__submission_set",
                "lessons__assignment_set__submission_set__student",
            ).all()
        
        # PENTING: Lakukan evaluasi queryset ke list agar data ter-fetch sekarang
        # Jika tidak di-list(), Django hanya menyimpan "query SQL"-nya, bukan datanya.
        data = list(queryset)

        # 3. Simpan ke Redis
        cache.set(self.KEY_LIST, data, self.TIMEOUT)
        
        return data

    def get_course_by_id(self, course_id: int):
        key = self.KEY_DETAIL.format(course_id)
        
        # 1. Cek Redis
        cached_data = cache.get(key)
        if cached_data:
            return cached_data

        # 2. Query DB
        course = get_object_or_404(
            Course.objects.prefetch_related(
                "lessons",
                "lessons__assignment_set",
                "lessons__assignment_set__submission_set",
                "lessons__assignment_set__submission_set__student"
            ), 
            id=course_id
        )

        # 3. Simpan ke Redis
        cache.set(key, course, self.TIMEOUT)
        
        return course

    def create_course(self, **data):
        # Create Data
        course = Course.objects.create(**data)
        
        cache.delete(self.KEY_LIST)
        cache.delete(self.KEY_STATS)
        
        return course

    def update_course(self, course_id, file_data=None, **data):
        course = get_object_or_404(Course, id=course_id)
        
        # Update field text
        for key, value in data.items():
            setattr(course, key, value)
        
        # Update file (thumbnail) jika ada
        if file_data:
            if course.thumbnail:
                course.thumbnail.delete(save=False)
            course.thumbnail = file_data

        course.save()
        cache.delete(self.KEY_LIST)
        cache.delete(self.KEY_DETAIL.format(course_id))

        return course

    def delete_course(self, course_id):
        course = get_object_or_404(Course, id=course_id)
        course.delete()

        # INVALIDASI CACHE
        cache.delete(self.KEY_LIST)
        cache.delete(self.KEY_DETAIL.format(course_id))
        cache.delete(self.KEY_STATS)