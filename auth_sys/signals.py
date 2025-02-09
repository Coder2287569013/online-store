from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            admin_group, _ = Group.objects.get_or_create(name='Administrator')
            admin_group.user_set.add(instance)
        else:
            customer_group, _ = Group.objects.get_or_create(name='Customer')
            customer_group.user_set.add(instance)