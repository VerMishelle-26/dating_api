from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Like, ProfileView, DateInvitation

User = get_user_model()


class LikeSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "from_user", "to_user", "type", "created_at"]
        read_only_fields = ["id", "from_user", "created_at"]


class ProfileViewSerializer(serializers.ModelSerializer):
    viewer = serializers.StringRelatedField(read_only=True)
    viewed = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ProfileView
        fields = ["id", "viewer", "viewed", "viewed_at"]
        read_only_fields = ["id", "viewed_at"]


class DateInvitationSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField(read_only=True)
    to_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DateInvitation
        fields = ["id", "from_user", "to_user", "message", "status", "created_at"]
        read_only_fields = ["id", "from_user", "created_at"]