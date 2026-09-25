from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LikeViewSet, RandomProfileView, ProfileViewHistoryViewSet, DateInvitationViewSet,
)

router = DefaultRouter()
router.register("likes", LikeViewSet, basename="like")
router.register("views", ProfileViewHistoryViewSet, basename="view")
router.register("invitations", DateInvitationViewSet, basename="invitation")
router.register("random", RandomProfileView, basename="random")

urlpatterns = [
    path("", include(router.urls)),
]