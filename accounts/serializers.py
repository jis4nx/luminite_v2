from django.http.response import json
from rest_framework import serializers

from shop.models.user import UserProfile
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "type", "password", "password2"]

        extra_kwargs = {
            "password": {"write_only": True},
            "style": {"input_type": "password"},
        }

    def save(self):
        user = User(
            email=self.validated_data["email"], type=self.validated_data["type"]
        )
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords must match."})
        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

    def to_representation(self, instance):
        user = self.context['request'].user
        rep = super().to_representation(instance)
        rep['user'] = {'email': user.email}
        return rep
