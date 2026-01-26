from ninja import Schema

class MahasiswaStatsOut(Schema):
    total_mahasiswa: int

class MahasiswaIn(Schema):
    name: str
    nim: str
    angkatan: int
    program_studi: str

class MahasiswaUpdate(Schema):
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

    @staticmethod
    def resolve_role(obj):
        return obj.user.role if hasattr(obj.user, 'role') else "mahasiswa"

class SuccessSchema(Schema):
    success: bool
    message: str