# apps/accounts/services.py
from django.core.cache import cache
from .models import User

class UserService:
    KEY_STATS = "users:stats"
    TIMEOUT = 60 * 60 
    def get_user_stats(self):
        data = cache.get(self.KEY_STATS)
        if data:
            return data

        total_users = User.objects.count()
        total_mahasiswa = User.objects.filter(role=User.Role.Mahasiswa).count()
        total_dosen = User.objects.filter(role=User.Role.DOSEN).count()
        total_admin = User.objects.filter(role=User.Role.ADMIN).count()

        data = {
            "total_users": total_users,
            "total_user_mahasiswa": total_mahasiswa,
            "total_user_dosen": total_dosen,
            "total_user_admin": total_admin
        }

        cache.set(self.KEY_STATS, data, self.TIMEOUT)
        
        return data

    def invalidate_stats(self):
        """Hapus cache saat ada user create/delete"""
        cache.delete(self.KEY_STATS)