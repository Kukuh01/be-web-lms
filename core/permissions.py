def admin_only(request):
    if request.user.role != "admin":
        return 403, {"detail": "Admin only"}
    
def dosen_only(request):
    if request.user.role != "dosen":
        return 403, {"detail":"Dosen only"}
    
def mahasiswa_only(request):
    if request.user.role != "mahasiswa":
        return 403, {"detail": "Mahasiswa only"}