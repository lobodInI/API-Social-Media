import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "social_media", "posts", filename)


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        get_user_model(),
        related_name="posts",
        on_delete=models.CASCADE,
    )
    hashtag = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField()
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=post_image_file_path,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ["-created_at",]


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="likes",
    )
