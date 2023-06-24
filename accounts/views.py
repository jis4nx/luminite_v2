from django.http import JsonResponse
from django.http.response import json
from django.middleware.csrf import CSRF_SESSION_KEY
from django.views import generic
from rest_framework.generics import CreateAPIView, mixins
from rest_framework.response import Response
from .serializers import AddressSerializer, RegisterSerializer, UserProfileSerializer
from .models import User
from LuminiteV2.settings import SIMPLE_JWT
from rest_framework_simplejwt.views import TokenObtainPairView, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import status
from datetime import datetime
from rest_framework.views import APIView
from shop.models.user import Address, UserProfile


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
            secure=False,
            expires=datetime.now() + SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        )
        res.set_cookie(
            key="refresh",
            value=token_refresh,
            httponly=True,
            secure=False,
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
        res.delete_cookie('refresh')
        return res


class VerifyToken(APIView):
    def get(self, request):
        token = request.COOKIES.get("refresh")
        if not token:
            return Response({'error': 'Refresh token is missing!'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(token).verify()
        except InvalidToken:
            return Response({'error': 'invalid refresh token'},
                            status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': 'Something went wrong!'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'success': 'refresh token is valid'},
                        status=status.HTTP_200_OK)


class TokenExpiration(APIView):
    def get(self, request):
        resp = {"access": False, "refresh": False}
        token_access = request.COOKIES.get('access')
        token_refresh = request.COOKIES.get('refresh')
        if token_access:
            resp['access'] = True
        if token_refresh:
            resp['refresh'] = True
        return Response(resp)


class ProfileView(APIView):
    def get(self, request):
        if not self.request.user.is_anonymous:
            profile = UserProfile.objects.get(user=self.request.user)
            serializer = UserProfileSerializer(
                profile, context={'request': request})
            return Response(serializer.data)
        return Response({'error': 'user is not authenticated!'},
                        status=status.HTTP_401_UNAUTHORIZED)


class AddressView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
