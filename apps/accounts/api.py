from typing import Union, List
from ninja import Router, Schema
from ninja.errors import HttpError
from django.contrib.auth import authenticate
from .models import User
from .schemas import LoginSchema, TokenSchema
from .auth import create_access_token
from core.jwt_auth import JWTAuth
from typing import Optional
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from core.permissions import admin_only
from enum import Enum

# Asumsi import model dan schema lain sudah benar
from apps.user.mahasiswa.api import MahasiswaOut
from apps.user.mahasiswa.models import Mahasiswa
from apps.user.dosen.api import DosenOut
from apps.user.dosen.models import Dosen

from .services import UserService

router = Router(tags=["Accounts Management"])

# --- Account Schema ---
class ErrorSchema(Schema):
    detail: str

class AdminOut(Schema):
    name: str
    role: str = "admin"

class UserRoleEnum(str, Enum):
    admin = "admin"
    dosen = "dosen"
    mahasiswa = "mahasiswa"

# Schema untuk Input Pembuatan User Baru
class UserCreateSchema(Schema):
    username: str
    password: str
    role: UserRoleEnum  # <--- Tambahkan ini
    is_staff: bool = False

# Schema untuk Update User (Password opsional)
class UserUpdateSchema(Schema):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRoleEnum] = None # <--- Tambahkan ini (opsional)
    is_active: Optional[bool] = None

# Schema Output (Menampilkan ID untuk dipakai di step selanjutnya)
class UserOut(Schema):
    id: int
    username: str
    role: str
    is_active: bool
    is_staff: bool

class UserStatsOut(Schema):
    total_users: int
    total_user_mahasiswa: int
    total_user_dosen: int
    total_user_admin: int

@router.post("/login", response={200: TokenSchema, 401: ErrorSchema})
def login(request, data: LoginSchema):
    user = authenticate(
        username=data.username,
        password=data.password
    )
    if not user:
        raise HttpError(401, "Invalid credentials")
    
    token = create_access_token(user)
    return 200, {"access": token}


@router.get(
    "/me",
    response={200: Union[MahasiswaOut, DosenOut, AdminOut], 404: ErrorSchema},
    auth=JWTAuth()
)
def get_me(request):
    user = request.auth

    mahasiswa = Mahasiswa.objects.filter(user=user).first()
    if mahasiswa:
        return 200, mahasiswa

    dosen = Dosen.objects.filter(user=user).first()
    if dosen:
        return 200, {
            "id": dosen.id,
            "name": dosen.name,
            "nidn": dosen.nidn,
            "fakultas": dosen.fakultas,
            "role": "dosen"
        }

    if user.is_staff or user.is_superuser:
        return 200, {
            "name": user.username,
            "role": "admin"
        }
    
    raise HttpError(404, "Profile not found")

user_service = UserService()
@router.get("/stats", response=UserStatsOut, auth=JWTAuth())
def get_user_statistics(request):
    """
    Mengambil jumlah user total dan per role.
    Data diambil dari Cache Redis.
    """
    admin_only(request)
    return user_service.get_user_stats()

@router.get("/", response=List[UserOut], auth=JWTAuth())
def list_users(request):
    """
    List semua user untuk memudahkan Admin mencari ID saat mau create profil.
    """
    admin_only(request) # Hanya admin yang boleh lihat
    return User.objects.all()

@router.post("/", response={201: UserOut, 400: ErrorSchema}, auth=JWTAuth())
def create_user(request, data: UserCreateSchema):
    """
    Langkah 1: Membuat Akun User (Username & Password).
    Output ID dari sini akan dipakai di API Mahasiswa/Dosen.
    """
    admin_only(request)

    # Validasi Username Unik
    if User.objects.filter(username=data.username).exists():
        return 400, {"detail": "Username sudah digunakan"}

    try:
        # create_user otomatis meng-hash password
        is_staff_status = data.is_staff
        if data.role == "admin":
            is_staff_status = True

        user = User.objects.create_user(
            username=data.username,
            password=data.password,
            is_staff=is_staff_status,
            role=data.role  # <--- Simpan Role di sini
        )

        user_service.invalidate_stats()

        return 201, user
    except Exception as e:
        return 400, {"detail": str(e)}

@router.put("/{user_id}", response={200: UserOut, 404: ErrorSchema}, auth=JWTAuth())
def update_user(request, user_id: int, data: UserUpdateSchema):
    """
    Ganti Password atau Username user.
    """
    admin_only(request)
    user = get_object_or_404(User, id=user_id)

    # Update Username
    if data.username and data.username != user.username:
        if User.objects.filter(username=data.username).exists():
             raise HttpError(400, "Username already taken")
        user.username = data.username

    # Update Password (PENTING: Harus di-hash)
    if data.password:
        user.set_password(data.password)

    # Update Status Active
    if data.is_active is not None:
        user.is_active = data.is_active

    user.save()
    return 200, user

@router.delete("/{user_id}", auth=JWTAuth())
def delete_user(request, user_id: int):
    """
    Menghapus User.
    Efek Samping: Data Mahasiswa/Dosen terkait akan ikut terhapus (CASCADE).
    """
    admin_only(request)
    user = get_object_or_404(User, id=user_id)
    
    # Proteksi: Jangan biarkan admin menghapus dirinya sendiri
    if user.id == request.auth.id:
        raise HttpError(400, "Anda tidak bisa menghapus akun anda sendiri")

    user.delete()
    user_service.invalidate_stats()
    
    return {"success": True, "message": "User berhasil dihapus"}