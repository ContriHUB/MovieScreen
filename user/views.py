import requests
import os
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Show, Movies
from django.utils import timezone
from .forms import ShowForm
from django.views import View
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

API_KEY = os.getenv('API_KEY')

def shows(request):
    shows = Show.objects.all().order_by('-time')
    return render(request, 'shows.html', {'shows': shows})

class MovieAutocomplete(View):
    def get(self, request):
        query = request.GET.get('query', '')
        print(f"Query received: {query}") 
        if query:
            ##########
            api=API_KEY
            ##########
            url = f"http://www.omdbapi.com/?s={query}&apikey={api}"
            response = requests.get(url)
            data = response.json()
            print(f"API response: {data}") 
        
            if data.get('Response') == 'True':
                titles = [movie['Title'] for movie in data.get('Search', [])]
                return JsonResponse(titles, safe=False)
            else:
            
                return JsonResponse([], safe=False)
        return JsonResponse([], safe=False)


# it will fetch data from api if only title field is  provided
@staff_member_required
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        
        if Movies.objects.filter(title=title).exists():
            return render(request, 'add_movie.html', {'error_message': 'Movie already exists!'})

        # only title is provided  fetch data from the API
        if title :
            ############
            api_key =API_KEY
            ############
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
                    available=True
                )
                movie.poster.save(f"{title}_poster.jpg", File(img_temp)) 
                movie.save()

                return redirect('user:movie_list') 
            
            else:
                # movie not found
                error_message = data.get('Error', 'Movie not found.')
                return render(request, 'add_movie.html', {'error_message': error_message})

    
        else:
           return redirect('user:movie_list')

    else:
        return render(request, 'add_movie.html')


def movie_list(request):
    movies = Movies.objects.all()
    return render(request, 'movie_list.html', {'movies': movies})


@method_decorator(staff_member_required, name="dispatch")
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
