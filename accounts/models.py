from django.db import models


class Profile(models.Model):
    telegram_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    photo = models.ImageField(blank=True, null=True, upload_to="media/photos")

    def __str__(self):
        return self.username
