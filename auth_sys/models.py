from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    avatar = models.FileField(upload_to='avatars/', blank=True, null=True, default='avatars/default_avatar.png')
    reviews = models.FloatField(max_length=2, blank=True, null=True)
