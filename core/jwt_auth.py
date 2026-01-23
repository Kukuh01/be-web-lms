# =========================================================
# Deskripsi Program:
# Implementasi autentikasi berbasis JSON Web Token (JWT)
# menggunakan HttpBearer dari Django Ninja.
#
# Kelas JWTAuth digunakan untuk:
# - Mengekstrak token JWT dari header Authorization
# - Memvalidasi token JWT
# - Mengambil data user berdasarkan payload token
# - Menyimpan user yang terautentikasi ke dalam request
# =========================================================

# Import kelas HttpBearer untuk autentikasi Bearer Token
from ninja.security import HttpBearer

# Import library JWT untuk decoding dan validasi token
from jose import jwt, JWTError

# Import konfigurasi global Django
from django.conf import settings

# Import model User dari aplikasi accounts
from apps.accounts.models import User


class JWTAuth(HttpBearer):
    """
    Kelas autentikasi JWT berbasis HttpBearer.

    Kelas ini akan otomatis dipanggil oleh Django Ninja
    saat endpoint API menggunakan authentication=JWTAuth().
    """

    def authenticate(self, request, token):
        """
        Method authenticate digunakan untuk memverifikasi token JWT
        dan mengembalikan user yang valid.

        Parameter:
        - request : objek HTTP request
        - token   : JWT token yang diambil dari header Authorization

        Return:
        - user  : jika token valid dan user ditemukan
        - None  : jika token tidak valid atau user tidak ditemukan
        """

        # Mencoba mendekode token JWT menggunakan secret dan algoritma
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,               # Secret key JWT
                algorithms=[settings.JWT_ALGORITHM] # Algoritma JWT
            )
        except JWTError:
            # Token tidak valid / expired
            return None

        # Mengambil data user berdasarkan user_id di payload token
        try:
            user = User.objects.get(id=payload["user_id"])
        except User.DoesNotExist:
            # User tidak ditemukan di database
            return None

        # Menyimpan user terautentikasi ke dalam request
        request.user = user

        # Mengembalikan user sebagai tanda autentikasi berhasil
        return user
