from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
# this model will appear in adminsite

# this is for admin listview metadata
class AdminPostListView(SummernoteModelAdmin, ModelAdmin):
    list_display = ('title', 'status', 'created_on', 'updated_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    summernote_fields = ('content',)

admin.site.register(Post, AdminPostListView)
