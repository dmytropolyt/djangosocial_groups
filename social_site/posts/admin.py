from django.contrib import admin
from .models import Post, PostImage


class PostImageInLine(admin.StackedInline):
    model = PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInLine]


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ['image']

