import os

from PIL import Image
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import redirect
from django.utils import timezone


def upload_user_image(instance, filename):
    file_path = os.path.join(os.path.join('users', str(instance.id), filename))
    return file_path


class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password, **extra_fields):
        return self._create_user(email, username, password, False, False, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        user = self._create_user(email, username, password, True, True, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    firstname = models.CharField(max_length=254, null=True, blank=True)
    lastname = models.CharField(max_length=254, null=True, blank=True)
    username = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField(max_length=1500, null=True, blank=True)

    image = models.ImageField(upload_to=upload_user_image, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_absolute_url(self):
        pass

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return redirect('user:profile', self.id)


@receiver(post_save, sender=User)
def save_img(sender, instance, **kwargs):
    if not instance.image:
        return
    img = Image.open(instance.image)
    (width, height) = img.size
    "Max width and height 800"
    if (300 / width < 300 / height):
        factor = 300 / height
    else:
        factor = 300 / width
    size = (int(width // factor), int(height // factor))
    img.resize(size, Image.ANTIALIAS)
    img.save(instance.image.path)
    img.close()
