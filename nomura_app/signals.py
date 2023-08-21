from .models import Client, CustomUser

from django.contrib.auth.models import User

from django.db.models.signals import post_save

from django.dispatch import receiver

from django.conf import settings

from django.contrib.auth.models import AbstractUser, BaseUserManager


@receiver(post_save, sender=CustomUser)
def post_save_create_client(sender, instance, created, *args, **kwargs):
	if created:
		Client.objects.create(user=instance, first_name=instance.first_name, last_name= instance.last_name, email_address= instance.email,)
