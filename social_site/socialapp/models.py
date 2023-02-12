from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import template
from PIL import Image
import misaka
import os

User = get_user_model()

register = template.Library()


class Group(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Groups', slugify(self.slug), 'main', instance)
        return None

    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User, related_name='own_groups', on_delete=models.CASCADE)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    created = models.DateTimeField(auto_now=True)
    members = models.ManyToManyField(User, through='GroupMember')
    image = models.ImageField(default='default/group_default.jpg', upload_to=image_upload_to, max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

        self.members.add(self.owner)

        img = Image.open(self.image.path)
        if img.height > 360 or img.width > 360:
            img.thumbnail((360, 360))
            img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('socialapp:single', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
