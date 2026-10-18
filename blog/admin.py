from django.contrib import admin

from .models import BlogEntry

@admin.register(BlogEntry)
class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'is_published', 'views_count')
    list_filter = ('is_published',)
    search_fields = ('title', 'content')
