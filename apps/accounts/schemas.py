from ninja import Schema
from typing import Optional
from enum import Enum

class AdminOut(Schema):
    name: str
    role: str

class DosenOut(Schema):
    id: int
    name: str
    nidn: str
    fakultas: str

    class Config:
        orm_mode = True

class MahasiswaOut(Schema):
    id: int
    name: str
    nim: str
    angkatan: int
    program_studi: str

    class Config:
        orm_mode = True

class LoginSchema(Schema):
    username: str
    password: str

class TokenSchema(Schema):
    access: str

class ErrorSchema(Schema):
    detail: str

class SuccessSchema(Schema):
    success: bool
    message: str

class AdminOut(Schema):
    name: str
    role: str = "admin"

class UserRoleEnum(str, Enum):
    admin = "admin"
    dosen = "dosen"
    mahasiswa = "mahasiswa"

class UserCreateSchema(Schema):
    username: str
    password: str
    role: UserRoleEnum
    is_staff: bool = False

class UserUpdateSchema(Schema):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRoleEnum] = None
    is_active: Optional[bool] = None

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