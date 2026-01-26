from typing import List, Union
from ninja import Router
from .models import User
from .auth import create_access_token
from core.jwt_auth import JWTAuth
from core.permissions import admin_only
from .schemas import LoginSchema, TokenSchema, ErrorSchema, UserCreateSchema, UserUpdateSchema, UserOut, UserStatsOut, AdminOut, MahasiswaOut, DosenOut, SuccessSchema
from .services import UserService

router = Router(tags=["Accounts Management"])
user_service = UserService()

@router.post("/login", response={200: TokenSchema, 401: ErrorSchema})
def login(request, data: LoginSchema):
    user = user_service.login(
        username=data.username,
        password=data.password
    )

    token = create_access_token(user)
    return 200, {"access": token}

@router.get(
    "/me",
    response=Union[MahasiswaOut, DosenOut, AdminOut],
    auth=JWTAuth()
)
def get_me(request):
    role, profile = user_service.get_profile(request.auth)

    if role == User.Role.Mahasiswa:
        return MahasiswaOut.from_orm(profile)

    if role == User.Role.DOSEN:
        return DosenOut.from_orm(profile)

    return AdminOut(
        name=profile.username,
        role="admin"
    )

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
    admin_only(request)
    return User.objects.all()

@router.post("/", response={201: UserOut}, auth=JWTAuth())
def create_user(request, data: UserCreateSchema):
    """
    Membuat Akun User (Username & Password).
    Output ID dari sini akan dipakai di API Mahasiswa/Dosen.
    """
    admin_only(request)
    user = user_service.create_user(data)
    return 201, user

@router.put("/{user_id}", response={200: UserOut}, auth=JWTAuth())
def update_user(request, user_id: int, data: UserUpdateSchema):
    """
    Ganti Password atau Username user.
    """
    admin_only(request)
    user = user_service.update_user(user_id, data)
    return 200, user

@router.delete("/{user_id}", response={ 400: ErrorSchema, 200: SuccessSchema}, auth=JWTAuth())
def delete_user(request, user_id: int):
    """
    Menghapus User.
    Efek Samping: Data Mahasiswa/Dosen terkait akan ikut terhapus (CASCADE).
    """
    admin_only(request)

    user_service.delete_user(
        target_user_id=user_id,
        actor_user_id=request.auth.id
    )

    return 200, {
        "success": True,
        "message": "User berhasil dihapus"
    }