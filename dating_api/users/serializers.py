from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Photo

User = get_user_model()


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "image", "is_main", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class UserSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "username", "first_name", "last_name", "full_name",
            "gender", "age", "city", "interests", "status", "privacy",
            "main_photo", "likes_count", "photos", "created_at",
        ]
        read_only_fields = ["id", "likes_count", "created_at", "photos"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "email", "username", "first_name", "last_name",
            "gender", "age", "city", "password", "password2",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        if attrs.get("age") and attrs["age"] < 18:
            raise serializers.ValidationError({"age": "Регистрация с 18 лет"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user