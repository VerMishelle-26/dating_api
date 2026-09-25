from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from .validators import validate_age, validate_no_contacts


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", "Мужской"
        FEMALE = "F", "Женский"
        OTHER = "O", "Другой"

    class Status(models.TextChoices):
        SEARCHING = "searching", "В поиске"
        BUSY = "busy", "Занят"
        FRIENDS = "friends", "Ищу друзей"
        RELATIONSHIP = "relationship", "В отношениях"

    class Privacy(models.TextChoices):
        PUBLIC = "public", "Публичный"
        FRIENDS = "friends", "Только для друзей"
        PRIVATE = "private", "Приватный"

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.OTHER,
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_age],
    )
    city = models.CharField(max_length=100, blank=True)
    interests = models.TextField(
        blank=True,
        help_text="Увлечения через запятую",
        validators=[validate_no_contacts],
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SEARCHING,
    )
    privacy = models.CharField(
        max_length=20,
        choices=Privacy.choices,
        default=Privacy.PUBLIC,
    )
    main_photo = models.ImageField(upload_to="avatars/", blank=True, null=True)
    likes_count = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Photo(models.Model):
    """Фотогалерея пользователя. Одна из фотографий — заглавная."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    image = models.ImageField(upload_to="photos/")
    is_main = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_main", "-uploaded_at"]

    def __str__(self):
        main = "main" if self.is_main else "extra"
        return f"Photo of {self.user.email} ({main})"

    def save(self, *args, **kwargs):
        # Если эта фотография — заглавная, снимем флаг с других
        if self.is_main:
            Photo.objects.filter(
                user=self.user, is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)