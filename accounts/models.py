from django.contrib.auth.models import AbstractUser

from django.db import models


class Profile(AbstractUser):
    telegram_id = models.IntegerField(unique=True, null=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    photo = models.ImageField(blank=True, null=True, upload_to="photo/")

    def __str__(self):
        return self.username
