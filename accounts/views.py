from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
from .models import User
from drf_spectacular.utils import extend_schema


class RegisterUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @extend_schema(
        summary="register a new user account",
        responses={200: RegisterSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)
