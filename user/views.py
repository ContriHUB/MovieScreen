import requests
from django.shortcuts import render, redirect
from .models import Show, Movies
from django.utils import timezone
from .forms import ShowForm
from django.views import View
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

def shows(request):
    shows = Show.objects.all().order_by('-time')
    return render(request, 'shows.html', {'shows': shows})

def home(request):
    return render(request, 'base.html')
# it will fetch data from api if only title field is  provided 
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        poster = request.FILES.get('poster') 
        available = request.POST.get('available', False) 

        # only title is provided  fetch data from the API
        if title and not description and not poster:
            api_key = # add it 
            url = f'http://www.omdbapi.com/?t={title}&apikey={api_key}'
            response = requests.get(url)
            data = response.json()

            if data['Response'] == 'True':
                description = data.get('Plot', 'No description available.')
                poster_url = data.get('Poster') 

                # Downloading the image 
                img_temp = NamedTemporaryFile()
                img_response = requests.get(poster_url)
                img_temp.write(img_response.content)
                img_temp.flush()

                # Creating  the movie object
                movie = Movies.objects.create(
                    title=title,
                    description=description,
                    available=available
                )
                movie.poster.save(f"{title}_poster.jpg", File(img_temp)) 
                movie.save()

                return redirect('user:movie_list') 
            
            else:
                # movie not found
                error_message = data.get('Error', 'Movie not found.')
                return render(request, 'add_movie.html', {'error_message': error_message})

    
        else:
            movie = Movies.objects.create(
                title=title,
                description=description,
                poster=poster, 
                available=available
            )
            movie.save()
            return redirect('user:movie_list')

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

class MovieListView(View):
    def get(self, request):
        movies = Movies.objects.all() 
        return render(request, 'movie_list.html', {'movies': movies}) 