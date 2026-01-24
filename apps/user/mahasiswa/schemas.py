from typing import Optional
from ninja import Schema

class MahasiswaStatsOut(Schema):
    total_mahasiswa: int

class MahasiswaIn(Schema):
    user_id: Optional[int] = None
    name: str
    nim: str
    angkatan: int
    program_studi: str

class MahasiswaOut(Schema):
    id: int
    name: str
    nim: str
    angkatan: int
    program_studi: str
    role: str = "mahasiswa"

    @staticmethod
    def resolve_role(obj):
        return obj.user.role if hasattr(obj.user, 'role') else "mahasiswa"