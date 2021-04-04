from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Profile(models.Model):
    django_user = models.OneToOneField(User, on_delete=models.CASCADE)
    paysafe_user_id = models.CharField(max_length=50, blank=True, default='')

    mobile = models.BigIntegerField(null=True)

    address = models.TextField(blank=True, default='')
    city = models.CharField(max_length=64, blank=True, default='')
    pincode = models.BigIntegerField(null=True)

    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return self.django_user.get_full_name()


# Django user post create
@receiver(pre_save, sender=User)
def fill_username(sender, instance, **kwargs):
    if instance.id is None:
        instance.username = instance.email


# Django user post create
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created and not Profile.objects.filter(django_user=instance).exists():
        Profile.objects.create(django_user=instance)
    instance.profile.save()
