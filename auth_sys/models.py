from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.
class CustomUser(AbstractUser):
    avatar = models.FileField(upload_to='avatars/', blank=True, null=True, default='avatars/default_avatar.png')

    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'avatars/default_avatar.png'
        super().save(*args, **kwargs)

        
class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="rating")
    rate = models.DecimalField(
        max_digits=2, 
        decimal_places=1, 
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        blank=False,
        null=False
    )
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)