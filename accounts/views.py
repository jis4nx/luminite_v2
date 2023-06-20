from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
from .models import User
from LuminiteV2.settings import SIMPLE_JWT
from rest_framework_simplejwt.views import TokenObtainPairView


"""Custom TokeObtainPairView"""


class CustomTokenPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        token = res.data['access']
        res.set_cookie(
            key="Token",
            value=token,
            httponly=True,
            expires=SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        )
        return res


class RegisterUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
