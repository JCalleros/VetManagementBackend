import jwt
import os
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token
from users.models import CustomUser

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        jwt_token = request.COOKIES.get('access_token')
        if not jwt_token:
            return None
        try:
            payload = jwt.decode(jwt_token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
            user_email = payload['email']
        except jwt.DecodeError:
            raise AuthenticationFailed('Invalid JWT token')
        
        try:
            user = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Invalid user')
                
        return (user, None)