from django.contrib import admin

from django.contrib.admin import register

from payments.models import Profile


@register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['django_user', 'paysafe_user_id', 'mobile', 'address', 'city', 'pincode', 'created', 'modified']
    readonly_fields = ['created', 'modified']
    autocomplete_fields = ['django_user']
