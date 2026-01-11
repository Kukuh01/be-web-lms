from ninja import Router, Schema
from .models import Dosen
from core.jwt_auth import JWTAuth
from core.permissions import admin_only
from typing import Optional
from django.shortcuts import get_object_or_404

router = Router(auth=JWTAuth(), tags=["Dosen"])

class DosenIn(Schema):
    user_id: Optional[int] = None
    name: str
    nidn: str
    fakultas: str

class DosenOut(Schema):
    id: int
    name: str
    nidn: str
    fakultas: str
    role: str = "dosen"

@router.get("/", response=list[DosenOut])
def list_dosen(request):
    return Dosen.objects.all()

@router.post("/")
def create_dosen(request, data: DosenIn):
    admin_only(request)
    payload = data.dict()
    if not payload.get('user_id'):
        payload.pop('user_id', None)
    try:
        mahasiswa = Dosen.objects.create(**payload)
        return {"id": mahasiswa.id, "message": "Dosen berhasil dibuat"}
    except Exception as e:
        return {"error": str(e)}, 400

@router.put("/{dsn_id}")
def update_dosen(request, dsn_id: int, data: DosenIn):
    admin_only(request)
    dosen = get_object_or_404(Dosen, id=dsn_id)

    payload = data.dict()
    if not payload.get('user_id'):
          payload.pop('user_id', None)
    try:
        for attr, value in payload.items():
            setattr(dosen, attr, value)

        dosen.save()
        return {"message": "Data dosen berhasil diperbarui"}
    except Exception as e:
            return {"error": str(e)}, 400
    
@router.delete("/{dsn_id}")
def delete_dosen(request, dsn_id: int):
    admin_only(request)
    try:
        dosen = get_object_or_404(Dosen, id=dsn_id)
        dosen.delete()
        return {"message": "Data dosen berhasil dihapus"}
    except Exception as e:
        return {"error": str(e)}, 400