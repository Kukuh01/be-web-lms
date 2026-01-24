from ninja import Schema
from typing import Optional

class DosenIn(Schema):
    user_id: Optional[int] = None
    name: str
    nidn: str
    fakultas: str

class DosenOut(Schema):
    id: int
    name: str
    nidn: str
    fakultas: str
    role: str = "dosen"

class DosenStatsOut(Schema):
    total_dosen: int