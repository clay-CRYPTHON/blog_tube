from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username fields is required")
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_password(username)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):

        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    username = models.CharField(
        _('Username'), max_length=200, unique=True
    )
    email = models.EmailField(max_length=200, null=True, blank=True, verbose_name='Email')
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/users/', default='user.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_author = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    telegram_link = models.URLField(max_length=200, null=True, blank=True)
    facebook_link = models.URLField(max_length=200, null=True, blank=True)
    instagram_link = models.URLField(max_length=200, null=True, blank=True)
    whatsapp_link = models.URLField(max_length=200, null=True, blank=True)
    github_link = models.URLField(max_length=200, null=True, blank=True)
    portfilo_link = models.URLField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ("created_at",)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def full_name(self):
        name = ''
        if self.last_name:
            name += self.last_name
        if self.first_name:
            name += (" " + self.first_name)
        return name

    def get_absolute_url(self):
        return f'/users/{self.uuid}'

    def get_update_url(self):
        return f'/users/{self.uuid}/update'

    def get_delete_url(self):
        return f'/users/{self.uuid}/delete'
