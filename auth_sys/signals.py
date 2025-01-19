from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if not instance.is_superuser and created:
        customer_group, _ = Group.objects.get_or_create(name='Customer')
        instance.groups.add(customer_group)
    else:
        admin_group, _ = Group.objects.get_or_create(name='Administrator')
        instance.groups.add(admin_group)