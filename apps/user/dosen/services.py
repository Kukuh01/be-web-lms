# apps/user/dosen/services.py
from django.core.cache import cache
from .models import Dosen

class DosenService:
    KEY_STATS = "dosen:stats"
    TIMEOUT = 60 * 60 

    def get_dosen_stats(self):
        stats = cache.get(self.KEY_STATS)
        if stats:
            return stats

        total = Dosen.objects.count()
        
        data = {
            "total_dosen": total
        }

        cache.set(self.KEY_STATS, data, self.TIMEOUT)
        
        return data

    def invalidate_stats(self):
        """Hapus cache saat ada dosen baru atau dihapus"""
        cache.delete(self.KEY_STATS)