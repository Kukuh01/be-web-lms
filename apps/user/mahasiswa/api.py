from ninja import Router
from .models import Mahasiswa
from core.jwt_auth import JWTAuth
from core.permissions import admin_only
from django.shortcuts import get_object_or_404
from .services import MahasiswaService
from .schemas import MahasiswaIn, MahasiswaOut, MahasiswaStatsOut, SuccessSchema, MahasiswaUpdate

router = Router(auth=JWTAuth(), tags=["Mahasiswa"])
mahasiswa_service = MahasiswaService()

@router.get("/stats", response=MahasiswaStatsOut)
def get_mahasiswa_stats(request):
    """
    Mengambil jumlah total mahasiswa dari Cache Redis.
    """
    admin_only(request)
    return mahasiswa_service.get_mahasiswa_stats()

@router.get("/", response=list[MahasiswaOut])
def list_mahasiswa(request):
    return Mahasiswa.objects.all()

@router.post("/", response={201: MahasiswaOut})
def create_mahasiswa(request, data: MahasiswaIn):
    admin_only(request)
    mahasiswa = mahasiswa_service.create_mahasiswa(**data.dict())
    return 201, mahasiswa

@router.put("/{mhs_id}", response={200: MahasiswaUpdate})
def update_mahasiswa(request, mhs_id: int, data: MahasiswaUpdate):
    admin_only(request)
    mahasiswa = mahasiswa_service.update_mahasiswa(mhs_id, **data.dict(exclude_unset=True))
    return 200, mahasiswa

@router.delete("/{mhs_id}", response={200: SuccessSchema})
def delete_mahasiswa(request, mhs_id: int):
    admin_only(request)
    mahasiswa_service.delete_mahasiswa(mhs_id)
    return 200, {
        "success": True,
        "message": "Mahasiswa berhasil dihapus"
    }
