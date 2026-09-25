from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import User, Photo


@receiver(post_delete, sender=User)
def delete_user_main_photo(sender, instance, **kwargs):
    if instance.main_photo:
        instance.main_photo.delete(save=False)


@receiver(post_delete, sender=Photo)
def delete_photo_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)