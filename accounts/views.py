from django.http import JsonResponse
from django.middleware.csrf import CSRF_SESSION_KEY
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from .models import User
from LuminiteV2.settings import SIMPLE_JWT
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from datetime import datetime
from rest_framework.views import APIView


"""Custom TokeObtainPairView"""


class CustomTokenPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        token_access = res.data['access']
        token_refresh = res.data['refresh']
        res.set_cookie(
            key="access",
            value=token_access,
            httponly=True,
            samesite='None',
            expires=datetime.now() + SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        )
        res.set_cookie(
            key="refresh",
            value=token_refresh,
            httponly=True,
            samesite='None',
            expires=datetime.now() + SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        )
        return res


class RegisterUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    def get(self, request):
        res = Response("Logging Out")
        res.delete_cookie('access')
        return res


class VerifyToken(APIView):
    pass
