from ninja import Schema

class DosenIn(Schema):
    name: str
    nidn: str
    fakultas: str

class DosenOut(Schema):
    id: int
    name: str
    nidn: str
    fakultas: str

class DosenStatsOut(Schema):
    total_dosen: int

class SuccessSchema(Schema):
    success: bool
    message: str