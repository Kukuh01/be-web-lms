from ninja import Router, Schema
from .models import Dosen
from core.jwt_auth import JWTAuth

router = Router(auth=JWTAuth(), tags=["Dosen"])

class DosenIn(Schema):
    user_id: int
    name: str
    nidn: str
    fakultas: str

class DosenOut(Schema):
    id: int
    user_id: int
    name: str
    nidn: str
    fakultas: str

@router.post("/")
def create_dosen(request, data: DosenIn):
    dosen = Dosen.objects.create(**data.dict())
    return {"id": dosen.id}

@router.get("/", response=list[DosenOut])
def list_dosen(request):
    return Dosen.objects.all()

