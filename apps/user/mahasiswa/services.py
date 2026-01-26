# apps/user/dosen/services.py
from django.core.cache import cache
from .models import Mahasiswa
from django.shortcuts import get_object_or_404

class MahasiswaService:
    KEY_STATS = "mahasiswa:stats"
    TIMEOUT = 60 * 60 

    def get_mahasiswa_stats(self):
        stats = cache.get(self.KEY_STATS)
        if stats:
            return stats

        total = Mahasiswa.objects.count()
        
        data = {
            "total_mahasiswa": total
        }

        cache.set(self.KEY_STATS, data, self.TIMEOUT)
        
        return data

    def invalidate_stats(self):
        """Hapus cache saat ada mahasiswa baru atau dihapus"""
        cache.delete(self.KEY_STATS)

    def create_mahasiswa(self, **data):
        mahasiswa = Mahasiswa.objects.create(**data)
        return mahasiswa

    def update_mahasiswa(request, mhs_id: int, **data):
        mahasiswa = get_object_or_404(Mahasiswa, id=mhs_id)

        for field, value in data.items():
            setattr(mahasiswa, field, value)
        mahasiswa.save()

        return mahasiswa
    
    def delete_mahasiswa(self, mhs_id: int):
        mahasiswa = get_object_or_404(Mahasiswa, id=mhs_id)
        
        mahasiswa.delete()
        
        return True