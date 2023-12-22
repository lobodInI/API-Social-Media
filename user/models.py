import os
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _
from django.db import models


def user_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.nickname)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "social_media", "users", filename)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, unique=True)
    user_image = models.ImageField(
        null=True,
        blank=True,
        upload_to=user_image_file_path,
    )
    city = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    date_registration = models.DateField(auto_now_add=True)
    username = None
    email = models.EmailField(
        _("email address",),
        unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserFollowing(models.Model):
    user_id = models.ForeignKey(
        get_user_model(),
        related_name="following",
        on_delete=models.CASCADE,
    )
    user_following = models.ForeignKey(
        get_user_model(),
        related_name="followers",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("user_id", "user_following",)
