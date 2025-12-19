from ninja.security import HttpBearer
from jose import jwt, JWTError
from django.conf import settings
from apps.accounts.models import User

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except JWTError:
            return None
        
        try:
            user = User.objects.get(id=payload["user_id"])
        except User.DoesNotExist:
            return None
        
        request.user = user
        return user