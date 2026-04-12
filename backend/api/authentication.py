from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken


class AgroUser:
    """Simple user object built from JWT claims — no DB lookup needed."""
    def __init__(self, username, role):
        self.username = username
        self.role = role
        self.is_authenticated = True
        self.is_active = True

    def __str__(self):
        return self.username


class AgroJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        username = validated_token.get('username')
        role = validated_token.get('role', 'user')
        if not username:
            raise InvalidToken('Token has no username')
        return AgroUser(username=username, role=role)
