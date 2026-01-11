from typing import Union, List
from ninja import Router, Schema
from ninja.errors import HttpError
from django.contrib.auth import authenticate
from .models import User
from .schemas import LoginSchema, TokenSchema
from .auth import create_access_token
from core.jwt_auth import JWTAuth

# Asumsi import model dan schema lain sudah benar
from apps.user.mahasiswa.api import MahasiswaOut
from apps.user.mahasiswa.models import Mahasiswa
from apps.user.dosen.api import DosenOut
from apps.user.dosen.models import Dosen

router = Router()

class ErrorSchema(Schema):
    detail: str

class AdminOut(Schema):
    name: str
    role: str = "admin"

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