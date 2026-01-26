# apps/accounts/services.py
from django.core.cache import cache
from .models import User
from apps.user.mahasiswa.models import Mahasiswa
from apps.user.dosen.models import Dosen
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

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

    def login(self, username: str, password: str):
        user = authenticate(username=username, password=password)
        if not user:
            raise HttpError(401, "Invalid credentials")
        return user
    
    def get_profile(self, user: User):
        """
        Ambil profile berdasarkan role user (RBAC murni)
        """
        if user.role == User.Role.Mahasiswa:
            profile = Mahasiswa.objects.filter(user=user).first()
            if not profile:
                raise HttpError(404, "Mahasiswa profile not found")
            return user.role, profile

        if user.role == User.Role.DOSEN:
            profile = Dosen.objects.filter(user=user).first()
            if not profile:
                raise HttpError(404, "Dosen profile not found")
            return user.role, profile

        if user.role == User.Role.ADMIN:
            return user.role, user

        raise HttpError(404, "Profile not found")

    def create_user(self, data):
        if User.objects.filter(username=data.username).exists():
            raise HttpError(400, "Username sudah digunakan")

        # create_user otomatis meng-hash password
        is_staff_status = data.is_staff
        if data.role == "admin":
            is_staff_status = True

        user = User.objects.create_user(
            username=data.username,
            password=data.password,
            is_staff=is_staff_status,
            role=data.role 
        )

        self.invalidate_stats()

        return user
    
    def update_user(self, user_id: int, data):
        """
        Ganti Password atau Username user.
        """
        user = get_object_or_404(User, id=user_id)

        # Update Username
        if data.username and data.username != user.username:
            if User.objects.filter(username=data.username).exists():
                raise HttpError(400, "Username already taken") #menghentikan eksekusi kode dan mengirim error ke pemanggilnya.
            user.username = data.username

        # Update Password (PENTING: Harus di-hash)
        if data.password:
            user.set_password(data.password)

        # Update Status Active
        if data.is_active is not None:
            user.is_active = data.is_active

        user.save()
        return user
    
    def delete_user(self, target_user_id: int, actor_user_id: int):
        """
        Menghapus user dengan proteksi:
        - Admin tidak boleh menghapus dirinya sendiri
        """
        user = get_object_or_404(User, id=target_user_id)

        if user.id == actor_user_id:
            raise HttpError(400, "Anda tidak bisa menghapus akun anda sendiri")

        user.delete()
        self.invalidate_stats()