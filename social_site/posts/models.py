from django.db import models
from django.urls import reverse
from django.utils.text import slugify
import misaka
import os
from socialapp.models import Group
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=50)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username, 'pk': self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']


class PostImage(models.Model):

    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join('Groups', slugify(self.post.group.slug), self.post.title, instance)

    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to=image_upload_to)


