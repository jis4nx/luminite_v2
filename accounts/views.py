from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer
from .models import User


class RegisterUser(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
