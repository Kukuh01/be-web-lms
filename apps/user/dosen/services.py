# apps/user/dosen/services.py
from django.core.cache import cache
from .models import Dosen
from django.shortcuts import get_object_or_404

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

    def create_dosen(self, **data):
        dosen = Dosen.objects.create(**data)
        return dosen

    def update_dosen(request, dsn_id: int, **data):
        dosen = get_object_or_404(Dosen, id=dsn_id)

        for attr, value in data.items():
            setattr(dosen, attr, value)
        dosen.save()

        return dosen
    
    def delete_dosen(self, dsn_id: int):
        dosen = get_object_or_404(Dosen, id=dsn_id)
        
        dosen.delete()
        
        return True