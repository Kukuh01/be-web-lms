# apps/user/dosen/services.py
from django.core.cache import cache
from .models import Mahasiswa

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