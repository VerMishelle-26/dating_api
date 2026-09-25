from django.conf import settings
from django.db import models


class Like(models.Model):
    """Лайк или дизлайк."""
    class Type(models.TextChoices):
        LIKE = "like", "Лайк"
        DISLIKE = "dislike", "Дизлайк"

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes_given"
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes_received"
    )
    type = models.CharField(max_length=10, choices=Type.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.from_user.email} → {self.to_user.email}: {self.type}"


class ProfileView(models.Model):
    """История просмотренных профилей."""
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="views_made"
    )
    viewed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="views_received"
    )
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-viewed_at"]

    def __str__(self):
        return f"{self.viewer.email} viewed {self.viewed.email}"


class DateInvitation(models.Model):
    """Приглашение на свидание / обмен контактами."""
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает"
        ACCEPTED = "accepted", "Принято"
        DECLINED = "declined", "Отклонено"

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="invitations_sent"
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="invitations_received"
    )
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.from_user.email} → {self.to_user.email} ({self.status})"