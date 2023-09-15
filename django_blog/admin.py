from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
# this model will appear in adminsite

# this is for admin listview metadata
class AdminPostListView(SummernoteModelAdmin, ModelAdmin):
    list_display = ('title', 'status', 'created_on', 'updated_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    summernote_fields = ('content',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

admin.site.register(Post, AdminPostListView)

