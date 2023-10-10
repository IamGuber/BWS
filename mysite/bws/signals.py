from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Buyer


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        username = instance.username
        email = instance.email
        Buyer.objects.create(name=username, email=email, user_client=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.buyer.save()
