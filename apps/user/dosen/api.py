from ninja import Router, Schema
from .models import Dosen
from core.jwt_auth import JWTAuth
from core.permissions import admin_only
from django.shortcuts import get_object_or_404
from .services import DosenService
from .schemas import DosenStatsOut, DosenOut, DosenIn, SuccessSchema

router = Router(auth=JWTAuth(), tags=["Dosen"])
dosen_service = DosenService()

@router.get("/stats", response=DosenStatsOut)
def get_dosen_stats(request):
    """
    Mengambil jumlah total dosen dari Cache Redis.
    """
    admin_only()
    return dosen_service.get_dosen_stats()

@router.get("/", response=list[DosenOut])
def list_dosen(request):
    admin_only(request)
    return Dosen.objects.all()

@router.post("/", response={201: DosenOut})
def create_dosen(request, data: DosenIn):
    admin_only(request)
    dosen = dosen_service.create_dosen(**data.dict())
    return 201, dosen

@router.put("/{dsn_id}", response={200: DosenOut})
def update_dosen(request, dsn_id: int, data: DosenIn):
    admin_only(request)
    dosen = dosen_service.update_dosen(dsn_id, **data.dict(exclude_unset=True))
    return 200, dosen
    
@router.delete("/{dsn_id}", response={200: SuccessSchema})
def delete_dosen(request, dsn_id: int):
    admin_only(request)
    dosen_service.delete_dosen(dsn_id)
    return 200, {
        "success": True,
        "message": "Dosen berhasil dihapus"
    }