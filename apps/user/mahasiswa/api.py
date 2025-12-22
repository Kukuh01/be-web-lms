from ninja import Router, Schema
from .models import Mahasiswa
from core.jwt_auth import JWTAuth
from core.permissions import admin_only

router = Router(auth=JWTAuth(), tags=["Mahasiswa"])

class MahasiswaIn(Schema):
    user_id: int
    name: str
    nim: str
    angkatan: str
    program_studi: str

class MahasiswaOut(Schema):
    id: int
    name: str
    nim: str
    angkatan: str
    program_studi: str

@router.post("/")
def create_mahasiswa(request, data: MahasiswaIn):
    admin_only(request)
    mahasiswa = Mahasiswa.objects.create(**data.dict())
    return {"id": mahasiswa.id}

@router.get("/", response=list[MahasiswaOut])
def list_mahasiswa(request):
    return Mahasiswa.objects.all()