from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.
class CustomUser(AbstractUser):
    avatar = models.FileField(upload_to='avatars/', blank=True, null=True, default='avatars/default_avatar.png')

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rating")
    rate = models.FloatField(max_length=2, blank=False, null=False)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)