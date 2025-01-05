from django.contrib import admin
from .models import AnimeMovie

@admin.register(AnimeMovie)
class AnimeMovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_date', 'author')
    search_fields = ('title', 'description', 'author')