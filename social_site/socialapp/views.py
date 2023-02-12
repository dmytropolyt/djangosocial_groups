from django.views.generic import TemplateView, CreateView, DetailView, ListView, View, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from .models import Group, GroupMember


class HomeView(TemplateView):
    template_name = 'socialapp/index.html'


class CreateGroup(LoginRequiredMixin, CreateView):
    fields = ('name', 'description', 'image')
    model = Group

    def form_valid(self, form):
        f = form.save(commit=False)
        f.owner = self.request.user
        f.save()
        return super().form_valid(form)


class UpdateGroup(PermissionRequiredMixin, UpdateView):
    model = Group
    fields = ['name', 'description', 'image']


class SingleGroup(DetailView):
    model = Group


class ListGroup(ListView):
    model = Group
    paginate_by = 5


class JoinGroup(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=request.user, group=group)
        except IntegrityError:
            messages.warning(request, 'Warning already a member!')
        else:
            messages.success(request, 'You are now a member!')

        # is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        # if is_ajax:
        members_count = group.members.count()
        return JsonResponse({'members_count': members_count})


class LeaveGroup(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        try:
            membership = GroupMember.objects.filter(
                user=request.user, group__slug=self.kwargs.get('slug')
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(request, "Sorry you aren't in this group!")
            print('dope')
        else:
            membership.delete()
            messages.success(request, 'You have left the group!')

        members_count = membership.group.members.count()
        return JsonResponse({'members_count': members_count})