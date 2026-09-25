from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Like, ProfileView, DateInvitation
from .serializers import (
    LikeSerializer,
    ProfileViewSerializer,
    DateInvitationSerializer,
)

User = get_user_model()


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return Like.objects.filter(
            from_user=self.request.user
        ).select_related("to_user")

    def perform_create(self, serializer):
        """Создаёт лайк/дизлайк, ловит дубликат."""
        try:
            serializer.save(from_user=self.request.user)
        except IntegrityError:
            raise ValidationError(
                {"detail": "Вы уже взаимодействовали с этим пользователем"}
            )

    @action(detail=False, methods=["get"])
    def liked(self, request):
        likes = self.get_queryset().filter(type="like")
        return Response(LikeSerializer(likes, many=True).data)

    @action(detail=False, methods=["get"])
    def disliked(self, request):
        dislikes = self.get_queryset().filter(type="dislike")
        return Response(LikeSerializer(dislikes, many=True).data)


class RandomProfileView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        qs = User.objects.exclude(id=request.user.id)

        gender = request.query_params.get("gender")
        city = request.query_params.get("city")
        status_ = request.query_params.get("status")
        age_min = request.query_params.get("age_min")
        age_max = request.query_params.get("age_max")

        if gender:
            qs = qs.filter(gender=gender)
        if city:
            qs = qs.filter(city__icontains=city)
        if status_:
            qs = qs.filter(status=status_)
        if age_min:
            qs = qs.filter(age__gte=age_min)
        if age_max:
            qs = qs.filter(age__lte=age_max)

        # Исключаем уже просмотренных
        viewed_ids = ProfileView.objects.filter(
            viewer=request.user
        ).values_list("viewed_id", flat=True)
        qs = qs.exclude(id__in=viewed_ids)

        user = qs.order_by("?").first()
        if not user:
            return Response(
                {"detail": "Нет подходящих профилей"},
                status=status.HTTP_404_NOT_FOUND,
            )

        ProfileView.objects.create(viewer=request.user, viewed=user)

        from users.serializers import UserSerializer

        return Response(UserSerializer(user).data)


class ProfileViewHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileViewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProfileView.objects.filter(
            viewer=self.request.user
        ).select_related("viewed")


class DateInvitationViewSet(viewsets.ModelViewSet):
    serializer_class = DateInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DateInvitation.objects.filter(
            from_user=self.request.user
        ).select_related("to_user")

    def perform_create(self, serializer):
        to_user_id = self.request.data.get("to_user")
        to_user = get_object_or_404(User, id=to_user_id)

        # Проверяем взаимный лайк
        if not Like.objects.filter(
            from_user=self.request.user, to_user=to_user, type="like"
        ).exists():
            raise permissions.PermissionDenied(
                "Сначала лайкните пользователя"
            )
        if not Like.objects.filter(
            from_user=to_user, to_user=self.request.user, type="like"
        ).exists():
            raise permissions.PermissionDenied(
                "Взаимного лайка нет"
            )

        serializer.save(from_user=self.request.user, to_user=to_user)