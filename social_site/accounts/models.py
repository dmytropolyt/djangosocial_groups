from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import os


class User(AbstractUser):

    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Users', self.username, instance)
        return None

    email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(default='default/user.png', upload_to=image_upload_to)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            img.thumbnail((300, 300))
            img.save(self.image.path)

    def __str__(self):
        return f'@{self.username}'


