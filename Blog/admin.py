from django.contrib import admin
from .models import Post,BlogComment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'updated_at')  # Customize list view in the admin
    search_fields = ('title', 'content')  # Add search functionality for title and content
    list_filter = ('updated_at',)  # Add filter options in the sidebar

admin.site.register(Post, PostAdmin)
admin.site.register(BlogComment)