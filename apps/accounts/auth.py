from datetime import datetime, timezone
from jose import jwt
from django.conf import settings
from django.contrib.auth import authenticate

def create_access_token(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "role": user.role,
        "exp": datetime.now(timezone.utc) + settings.JWT_ACCESS_TOKEN_EXPIRE,
    }

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)