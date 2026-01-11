from ninja import Router, Schema
from .models import Mahasiswa
from core.jwt_auth import JWTAuth
from core.permissions import admin_only
from typing import Optional
from django.shortcuts import get_object_or_404

router = Router(auth=JWTAuth(), tags=["Mahasiswa"])

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
    

@router.get("/", response=list[MahasiswaOut])
def list_mahasiswa(request):
    return Mahasiswa.objects.all()

@router.post("/")
def create_mahasiswa(request, data: MahasiswaIn):
    admin_only(request)
    payload = data.dict()
    if not payload.get('user_id'):
        payload.pop('user_id', None)
    try:
        mahasiswa = Mahasiswa.objects.create(**payload)
        return {"id": mahasiswa.id, "message": "Mahasiswa berhasil dibuat"}
    except Exception as e:
        return {"error": str(e)}, 400

@router.put("/{mhs_id}")
def update_mahasiswa(request, mhs_id: int, data: MahasiswaIn):
    admin_only(request)
    mahasiswa = get_object_or_404(Mahasiswa, id=mhs_id)

    payload = data.dict()
    if not payload.get('user_id'):
          payload.pop('user_id', None)
    try:
        for attr, value in payload.items():
            setattr(mahasiswa, attr, value)

        mahasiswa.save()
        return {"message": "Data mahasiswa berhasil diperbarui"}
    except Exception as e:
            return {"error": str(e)}, 400
    
@router.delete("/{mhs_id}")
def delete_mahasiswa(request, mhs_id: int):
    admin_only(request)
    try:
        mahasiswa = get_object_or_404(Mahasiswa, id=mhs_id)
        mahasiswa.delete()
        return {"message": "Data mahasiswa berhasil dihapus"}
    except Exception as e:
        return {"error": str(e)}, 400