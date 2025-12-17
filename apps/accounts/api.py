from ninja import Router, Schema
from .models import User

router = Router()

class UserOut(Schema):
    id: int
    username: str
    role: str

@router.get("/", response=list[UserOut])
def list_users(request):
    return User.objects.all()