from ninja import Router, Schema
from .models import User
from django.contrib.auth import authenticate
from .schemas import LoginSchema, TokenSchema
from .auth import create_access_token
from apps.user.mahasiswa.api import MahasiswaOut
from apps.user.mahasiswa.models import Mahasiswa
from core.jwt_auth import JWTAuth
from typing import Union

router = Router()

class AdminOut(Schema):
    name: str
    email: str
    role: str = "admin"

# class UserOut(Schema):
#     id: int
#     username: str
#     role: str

# @router.get("/", response=list[UserOut])
# def list_users(request):
#     return User.objects.all()

# router = Router(tags=["Auth"])

@router.post("/login", response=TokenSchema)
def login(request, data: LoginSchema):
    user = authenticate(
        username=data.username,
        password=data.password
    )
    if not user:
        return 401, {"detail": "Invalid credentials"}
    
    token = create_access_token(user)
    return {"access": token}

@router.get("/me", response={200: Union[MahasiswaOut, AdminOut]}, auth=JWTAuth())
def get_me(request):
    user = request.auth
    
    mahasiswa = Mahasiswa.objects.filter(user=user).first()
    if mahasiswa:
        return mahasiswa
    
    if user.is_staff or user.is_superuser:
        return {
            "name": user.username,
            "email": user.email,
            "role": "admin"
        }
    
    return 404, {"detail": "Profile not found"}