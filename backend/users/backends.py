import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = settings.TOKEN_PREFIX

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix != auth_header_prefix:
            return None

        return self.authenticate_credentials(request, token)

    def authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('This token has expired.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('This token is invalid.')

        try:
            user = User.objects.get(
                username=payload['sub'], token_identifier=payload['jti'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'This token is not associated with an account.')

        if user.is_banned:
            raise exceptions.AuthenticationFailed(
                'This account has been banned.')

        return user, token
