from django.contrib import admin
from .models import Group, GroupMember


class GroupMemberInLine(admin.TabularInline):
    model = GroupMember

    
admin.site.register(Group)
