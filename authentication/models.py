""" authentication Models """
from typing import Any
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)


class CustomAccountManager(BaseUserManager):
    """ Manager For management of new model """

    def create_user(self, email: str, username: str, first_name: str,
                    last_name: str, password: str, **other_fields: Any) -> Any:
        """ User Creation """
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, last_name=last_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, username: str, first_name: str,
                         last_name: str, password: str, **other_fields: Any):
        """ Superuser Creation """
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.'
            )
        return self.create_user(email, username, first_name, last_name,
                                password, **other_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ Customer User model """
    unique_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list = ['username', 'first_name', 'last_name']

    def __str__(self) -> str:
        return str(self.username)


def img_path(instance, filename):
    return f"{instance.User.username}/{filename}"


class Profile(models.Model):
    user = models.ForeignKey(User, related_name="owner",
                             on_delete=models.CASCADE)

    image = models.ImageField(
        upload_to=img_path, default="default/profile.jpg")
