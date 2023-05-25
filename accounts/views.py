from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
from .models import User
from drf_spectacular.utils import extend_schema


class RegisterUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
