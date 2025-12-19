from ninja import Router, Schema
from .models import User
from django.contrib.auth import authenticate
from .schemas import LoginSchema, TokenSchema
from .auth import create_access_token

router = Router()

class UserOut(Schema):
    id: int
    username: str
    role: str

@router.get("/", response=list[UserOut])
def list_users(request):
    return User.objects.all()

router = Router(tags=["Auth"])

@router.post("/login", response=TokenSchema)
def login(request, data: LoginSchema):
    user = authenticate(
        username=data.username,
        password=data.password
    )
    if not user:
        return 401, {"detail": "Invalid credentials"}
    
    token = create_access_token(user)
    return {"access": token}