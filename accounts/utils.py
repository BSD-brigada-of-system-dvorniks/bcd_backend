from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from .models import Token


def get_user_from_token(request):
    auth_header = get_authorization_header(request)
    if not auth_header:
        raise AuthenticationFailed('Authorization header is missing.')

    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != b'token':
        raise AuthenticationFailed('Authorization token is invalid.')

    token_key = parts[1].decode()
    
    try:
        token = Token.objects.get(key = token_key)
    except Token.DoesNotExist as exc:
        raise AuthenticationFailed('Invalid token.') from exc
    
    return token.user
