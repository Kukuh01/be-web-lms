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
from ninja.errors import HttpError
from apps.accounts.models import User

def admin_only(request):
    """
    Fungsi permission untuk membatasi akses hanya untuk user
    dengan role 'admin'.

    Parameter:
    - request : objek HTTP request yang berisi informasi user

    Return:
    - (403, detail) jika user bukan admin
    """
    user = request.auth
    if not user or user.role != User.Role.ADMIN:
        raise HttpError(403, "Admin only")


def dosen_only(request):
    """
    Fungsi permission untuk membatasi akses hanya untuk user
    dengan role 'dosen'.

    Parameter:
    - request : objek HTTP request yang berisi informasi user

    Return:
    - (403, detail) jika user bukan dosen
    """
    user = request.auth
    if not user or user.role != User.Role.DOSEN:
        raise HttpError(403, "Dosen only")

def mahasiswa_only(request):
    """
    Fungsi permission untuk membatasi akses hanya untuk user
    dengan role 'mahasiswa'.

    Parameter:
    - request : objek HTTP request yang berisi informasi user

    Return:
    - (403, detail) jika user bukan mahasiswa
    """
    user = request.auth
    if not user or user.role != User.Role.Mahasiswa:
        raise HttpError(403, "Mahasiswa only")


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
    user = request.auth
    if not user or user.role not in [
        User.Role.ADMIN,
        User.Role.DOSEN
    ]:
        raise HttpError(403, "Admin or Dosen only")