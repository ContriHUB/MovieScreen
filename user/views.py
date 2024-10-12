import requests
import os
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Show, Movies, Ticket
from django.utils import timezone
from .forms import ShowForm,UserRatingForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Count
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
            api = API_KEY
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

@staff_member_required
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        
        if Movies.objects.filter(title=title).exists():
            return render(request, 'add_movie.html', {'error_message': 'Movie already exists!'})

        if title:
            api_key = API_KEY
            url = f'http://www.omdbapi.com/?t={title}&apikey={api_key}'
            response = requests.get(url)
            data = response.json()

            if data['Response'] == 'True':
                description = data.get('Plot', 'No description available.')

                poster_url = data.get('Poster') 
                rating=data.get('imdbRating')
                if rating=='N/A':
                    rating=0
                rating = float(rating)
                stars = (rating / 10) * 5
                stars = round(stars * 2) / 2

                # Downloading the image 
                img_temp = NamedTemporaryFile()
                img_response = requests.get(poster_url)
                img_temp.write(img_response.content)
                img_temp.flush()

                # Creating the movie object
                movie = Movies.objects.create(
                    title=title,
                    description=description,
                    available=True,
                    stars=stars
                )
                movie.poster.save(f"{title}_poster.jpg", File(img_temp)) 
                movie.save()

                return redirect('user:movie_list') 
            
            else:
                error_message = data.get('Error', 'Movie not found.')
                return render(request, 'add_movie.html', {'error_message': error_message})

        else:
           return redirect('user:movie_list')
    else:
        return render(request, 'add_movie.html')

def movie_list(request):
    movies = Movies.objects.all()
    
    movie_data_list = []
    
    for movie in movies:
        
        latest_rating = movie.user_ratings.first()  
        movie_data = {
            'movie': movie,
            'latest_rating': latest_rating.stars if latest_rating else None, 
        }
        
        movie_data_list.append(movie_data)

    return render(request, 'movie_list.html', {'movie_data_list': movie_data_list})

def movie_review(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id) 
    if request.method == 'POST':
        form = UserRatingForm(request.POST)
        if form.is_valid():
            user_rating = form.save(commit=False)
            user_rating.movie = movie 
            existing_rating = movie.user_ratings.all() 
            if existing_rating:
                existing_rating.delete() 

            user_rating.save() 
            return redirect('user:movie_list') 
    else:
        form = UserRatingForm() 

    context = {
        'movie': movie,
        'latest_rating': movie.user_ratings.first(),  
        'form': form,
    }

    return render(request, 'review.html', context)  


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

@login_required
def book_ticket(request, show_id):
    show = Show.objects.get(id=show_id)

    # Get the list of seats that are already booked for this show
    booked_seats = Ticket.objects.filter(show=show).values_list('seat_number', flat=True)

    # Seat numbers from 1 to 100
    total_seats = range(1, 101)

    # Filter available seats (those not in the booked_seats list)
    available_seats = [seat for seat in total_seats if str(seat) not in booked_seats]

    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')

        # Check if the user has already booked this seat for the selected show
        if Ticket.objects.filter(user=request.user, show=show, seat_number=seat_number).exists():
            return render(request, 'book_ticket.html', {
                'show': show, 
                'available_seats': available_seats, 
                'error': 'You have already booked this seat.'
            })

        # Check if the user has already booked 2 tickets in the current month
        ticket_count = Ticket.objects.filter(
            user=request.user,
            booked_at__month=timezone.now().month,
            booked_at__year=timezone.now().year
        ).count()

        if ticket_count >= 2:
            return render(request, 'book_ticket.html', {
                'show': show, 
                'available_seats': available_seats, 
                'error': 'You can only book up to 2 tickets per month.'
            })

        # Ensure the selected seat is in the list of available seats
        if seat_number not in map(str, available_seats):
            return render(request, 'book_ticket.html', {
                'show': show, 
                'available_seats': available_seats, 
                'error': 'This seat is already booked or unavailable.'
            })

        # Book the ticket if everything is valid
        Ticket.objects.create(user=request.user, show=show, seat_number=seat_number)
        return redirect('user:shows')

    return render(request, 'book_ticket.html', {'show': show, 'available_seats': available_seats})


