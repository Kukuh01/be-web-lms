# =========================================================
# Deskripsi Program:
# Kumpulan fungsi permission (hak akses) untuk membatasi
# akses endpoint berdasarkan role user.
#
# Role yang didukung:
# - admin
# - dosen
# - mahasiswa
#
# Setiap fungsi akan memeriksa role user yang sedang login
# dan mengembalikan status error 403 jika tidak memiliki izin.
# =========================================================


def admin_only(request):
    """
    Fungsi permission untuk membatasi akses hanya untuk user
    dengan role 'admin'.

    Parameter:
    - request : objek HTTP request yang berisi informasi user

    Return:
    - (403, detail) jika user bukan admin
    """
    if request.user.role != "admin":
        return 403, {"detail": "Admin only"}


def dosen_only(request):
    """
    Fungsi permission untuk membatasi akses hanya untuk user
    dengan role 'dosen'.

    Parameter:
    - request : objek HTTP request yang berisi informasi user

    Return:
    - (403, detail) jika user bukan dosen
    """
    if request.user.role != "dosen":
        return 403, {"detail": "Dosen only"}


def mahasiswa_only(request):
    """
    Fungsi permission untuk membatasi akses hanya untuk user
    dengan role 'mahasiswa'.

    Parameter:
    - request : objek HTTP request yang berisi informasi user

    Return:
    - (403, detail) jika user bukan mahasiswa
    """
    if request.user.role != "mahasiswa":
        return 403, {"detail": "Mahasiswa only"}


def dosen_or_admin_only(request):
    """
    Fungsi permission untuk membatasi akses hanya untuk user
    dengan role 'dosen' atau 'admin'.

    Parameter:
    - request : objek HTTP request yang berisi informasi user

    Return:
    - (403, detail) jika user belum login atau tidak memiliki
      role yang sesuai
    - True jika user memiliki izin akses
    """
    user = request.user

    # Mengecek apakah user sudah login (terautentikasi)
    if not user.is_authenticated:
        return 403, {"detail": "Admin and Dosen only"}

    # Mengecek apakah role user termasuk dosen atau admin
    if user.role not in ["dosen", "admin"]:
        return 403, {"detail": "Admin and Dosen only"}

    # Akses diizinkan
    return True
