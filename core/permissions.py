def admin_only(request):
    if request.user.role != "admin":
        return 403, {"detail": "Admin only"}
    
def dosen_only(request):
    if request.user.role != "dosen":
        return 403, {"detail":"Dosen only"}
    
def mahasiswa_only(request):
    if request.user.role != "mahasiswa":
        return 403, {"detail": "Mahasiswa only"}
    
def dosen_or_admin_only(request):
    user = request.user

    if not user.is_authenticated:
        return 403, {"detail": "Admin and Dosen only"}
    
    if user.role not in ["dosen", "admin"]:
        return 403, {"detail": "Admin and Dosen only"}

    return True