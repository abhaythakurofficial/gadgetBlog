from django.shortcuts import render
from .models import AnimeMovie
from django.shortcuts import render, get_object_or_404

def anime_list(request):
    movies = AnimeMovie.objects.all()
    return render(request, 'movies/anime_list.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(AnimeMovie, id=movie_id)
    return render(request, 'movies/anime_detail.html', {'movie': movie})
