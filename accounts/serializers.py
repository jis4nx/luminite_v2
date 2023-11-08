from django.http.response import json
from rest_framework import serializers

from shop.models.user import Address, UserProfile
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

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
            raise serializers.ValidationError({"password": "Passwords must match."})
        user.set_password(password)
        user.save()
        return user


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

    def validate(self, attrs):
        user_profile = attrs["user_profile"]
        user_addresses = user_profile.addresses.count()
        if user_addresses > 5:
            raise serializers.ValidationError(
                "Maximum address limit reached for this user."
            )
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    def get_address(self, obj):
        address = Address.objects.filter(user_profile=obj, default=True).first()
        serializer = AddressSerializer(address)
        return serializer.data

    class Meta:
        model = UserProfile
        fields = ["id", "user", "image", "address"]

    def to_representation(self, instance):
        user = self.context["request"].user
        rep = super().to_representation(instance)
        rep["user"] = {"email": user.email}
        return rep
