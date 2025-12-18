from ninja import Router, Schema
from .models import Mahasiswa

router = Router()

class MahasiswaIn(Schema):
    user_id: int
    name: str
    nim: str
    program_studi: str

class MahasiswaOut(Schema):
    id: int
    name: str
    nim: str
    program_studi: str

@router.post("/")
def create_mahasiswa(request, data: MahasiswaIn):
    mahasiswa = Mahasiswa.objects.create(**data.dict())
    return {"id": mahasiswa.id}

@router.get("/", response=list[MahasiswaOut])
def list_mahasiswa(request):
    return Mahasiswa.objects.all()