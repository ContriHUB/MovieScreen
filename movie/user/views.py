from django.shortcuts import render, redirect
from .models import Show, Movies
from django.utils import timezone
from .forms import ShowForm
from django.views import View

def shows(request):
    upcoming_shows = Show.objects.all().order_by('-time')
    return render(request, 'shows.html', {'shows': upcoming_shows})

def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        poster = request.FILES.get('poster')
        available = request.POST.get('available', False)
        movie = Movies.objects.create(title=title, description=description, 
poster=poster, available=available)
        print(movie)
        movie.save
        
        return redirect('movie_list')
    else:
        return render(request, 'add_movie.html')

def movie_list(request):
    movies = Movies.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})


class AddShowView(View):
    form_class = ShowForm
    template_name = 'add_show.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user:shows')
        return render(request, self.template_name, {'form': form})
