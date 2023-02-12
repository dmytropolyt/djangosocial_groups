from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.http import Http404
from braces.views import SelectRelatedMixin
from .models import Post, PostImage
from .forms import PostForm, PostImageForm
from django.contrib.auth import get_user_model
from django.contrib import messages


User = get_user_model()


class PostList(SelectRelatedMixin, ListView):
    model = Post
    select_related = ('user', 'group')


class UserPosts(ListView):
    model = Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, DetailView):
    model = Post
    select_related = ('user', 'group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, CreateView):
    form_class = PostForm
    model = Post

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        files = self.request.FILES.getlist("image")
        f = form.save(commit=False)
        f.user = self.request.user
        f.save()

        for image in files:
            PostImage.objects.create(post=f, image=image)

        messages.success(self.request, 'Post has been added!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = PostImageForm
        return context

# Later I'll add opportunity to change post's images
class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'message']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, DeleteView):
    model = Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.pk)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)
