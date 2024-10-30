import requests
import os
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Show, Movies, Ticket,Reviews
from django.utils import timezone
from .forms import ShowForm
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
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import urlencode
from django.urls import reverse
from datetime import datetime
from better_profanity import profanity
from django.template.defaulttags import register
from notebook.recommender import recommend_by_genres

API_KEY = os.getenv('API_KEY')
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
genre_keywords = {
    'Action': ['fight', 'explosive', 'adventure', 'hero', 'battle', 'chase'],
    'Adventure': ['journey', 'exploration', 'quest', 'expedition', 'discover'],
    'Animation': ['animated', 'cartoon', 'family-friendly', 'animated film'],
    'Biography': ['biography', 'life story', 'based on a true story', 'real life'],
    'Comedy': ['comedy', 'humor', 'funny', 'laugh', 'joke', 'hilarious'],
    'Crime': ['crime', 'murder', 'detective', 'investigation', 'criminal'],
    'Documentary': ['documentary', 'real-life', 'non-fiction', 'informative'],
    'Drama': ['drama', 'emotional', 'realistic', 'relationship', 'conflict'],
    'Family': ['family', 'children', 'kid-friendly', 'parenting'],
    'Fantasy': ['fantasy', 'magical', 'imagination', 'supernatural'],
    'History': ['historical', 'based on history', 'period', 'historical drama'],
    'Horror': ['horror', 'scary', 'fright', 'ghost', 'haunted'],
    'Music': ['music', 'musical', 'song', 'dance', 'performance'],
    'Mystery': ['mystery', 'whodunit', 'puzzle', 'secret'],
    'Romance': ['romance', 'love', 'relationship', 'passion', 'affection'],
    'Sci-Fi': ['science fiction', 'space', 'futuristic', 'alien', 'technology'],
    'Sport': ['sports', 'competition', 'athlete', 'team'],
    'Thriller': ['thriller', 'suspense', 'tension', 'excitement'],
    'War': ['war', 'battlefield', 'soldier', 'military', 'combat'],
    'Western': ['western', 'cowboy', 'frontier', 'outlaw'],
}
def predict_genre(description):
    description = description.lower()
    for genre, keywords in genre_keywords.items():
        for keyword in keywords:
            if keyword in description:
                return genre  
    return 'Drama' 
@login_required
def shows(request):
    shows = Show.objects.all().order_by('-time')
    return render(request, 'shows.html', {'shows': shows})

@login_required
def movie_details(request):
    """
    DISPLAY A PAGE WITH DETAILS ABOUT THE MOVIE ON WHICH THE USER CLICKS
    ALSO SHOW LIST OF CAST MEMBERS
    """
    placeholder_poster = 'https://dancyflix.com/placeholder.png'
    id=request.GET.get('imdb_id','')
    movie=Movies.objects.filter(imdb_id=id)
    if movie:
        
        # FETCH THE CAST LIST OF THE MOVIE
        tmdb_api_key=TMDB_API_KEY
        url=f"https://api.themoviedb.org/3/movie/{id}/credits?api_key={tmdb_api_key}"
        response=requests.get(url)
        filtered_cast={}
        if response.status_code == 200:
            data=response.json()
            croplen=0
            if len(data['cast'])>=10:
                croplen=10
            else:
                croplen=len(data['cast'])
            filtered_cast = [
                {
                    'name': member['name'],
                    'character': member['character'],
                    'img_url' : f"https://image.tmdb.org/t/p/w200{member['profile_path']}"
                }
                for member in data['cast'][:croplen] if member['character']
            ]

        # fetch similar movies
        genres = list(map(lambda x: x.strip(), movie.first().genres.split(',')))
        similar_movies = recommend_by_genres(genres)
        similar_movies_poster_url = {}

        def get_omdb_title(similar_movie):
            title = similar_movie.split('(')[0].strip()
            if title.endswith(", The"):
                title = "The " + title[:-5].strip()
            return title

        for similar_movie in similar_movies:
            title = get_omdb_title(similar_movie)
            omdb_search_url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
            omdb_response = requests.get(omdb_search_url).json()
            poster = omdb_response.get('Poster')
            similar_movies_poster_url[similar_movie] = poster or placeholder_poster

        context={
            "movie":movie,
            "cast":filtered_cast,
            "similar_movies":similar_movies,
            "similar_movies_poster_url":similar_movies_poster_url
        }

    return render(request,'movie_details.html',context)

@method_decorator(login_required, name="dispatch")
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

@login_required
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
                imdb_rating = None
                critic_rating = None

                ratings = data.get('Ratings', [])

                for rating in ratings:
                    source = rating['Source']
                    value = rating['Value']

                    if source == 'Internet Movie Database':
                        imdb_rating = float(value.split('/')[0]) / 2  
                        print('imdb')

                    elif source == 'Metacritic':
                        critic_rating = float(value.split('/')[0]) / 20 
                        print('critic')
                    


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
                    age_rating=data["Rated"],
                    runtime=data["Runtime"],
                    rel_date=data["Released"],
                    director=data["Director"],
                    imdb_id=data["imdbID"],
                    genres=data["Genre"],
                    imdb_rating=round(imdb_rating, 1) if imdb_rating else None,
                    critic_rating=round(critic_rating, 1) if critic_rating else None,
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
    
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

genre_colors = {
    'Action': 'red',
    'Adventure': 'orange',
    'Animation': 'lightblue',
    'Biography': 'purple',
    'Comedy': 'yellow',
    'Crime': 'darkred',
    'Documentary': 'green',
    'Drama': 'blue',
    'Family': 'pink',
    'Fantasy': 'lightgreen',
    'History': 'brown',
    'Horror': 'black',
    'Music': 'cyan',
    'Mystery': 'darkblue',
    'Romance': 'magenta',
    'Sci-Fi': 'teal',
    'Sport': 'gold',
    'Thriller': 'darkviolet',
    'War': 'olive',
    'Western': 'tan',
}  
@login_required
def movie_list(request):
    movies = Movies.objects.all()
    print(movies)
    for movie in movies:
        movie.genre = predict_genre(movie.description) 
        print(movie.genre) 
        movie.color = genre_colors.get(movie.genre, '#ccc')  
        movie.save()  
    
    return render(request, 'movie_list.html', {'movies': movies})


@method_decorator(login_required, name="dispatch")
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
    booked__seats = list(map(int, Ticket.objects.filter(show=show).values_list('seat_number', flat=True)))

    booked_percentage = booked_seats.count()
    #condition to check whether to show notification or not
    show_toastr = booked_percentage >= 85

    # Seat numbers from 1 to 100
    total_seats = range(1, 101)
    all_seats = list(range(1, 101))
    seat_rows = [all_seats[i:i+10] for i in range(0, len(all_seats), 10)]

    # Filter available seats (those not in the booked_seats list)
    available_seats = [seat for seat in total_seats if str(seat) not in booked_seats]


    if request.method == 'POST':
        seat_numbers = request.POST.getlist('seat_numbers')  # Get the list of selected seats

        # Check if user has already booked these seats for the selected show
        existing_bookings = Ticket.objects.filter(user=request.user, show=show, seat_number__in=seat_numbers)

        if existing_bookings.exists():
            return render(request, 'book_ticket.html', {
                'show': show,
                'available_seats': available_seats,
                'error': 'You have already booked one or more of these seats.'
            })

        # Check if the user has already booked 2 tickets in the current month
        ticket_count = Ticket.objects.filter(
            user=request.user,
            booked_at__month=timezone.now().month,
            booked_at__year=timezone.now().year
        ).count()

        if ticket_count + len(seat_numbers) > 2:
            return render(request, 'book_ticket.html', {
                'show': show,
                'available_seats': available_seats,
                'error': 'You can only book up to 2 tickets per month.'
            })

        # Ensure all selected seats are available
        unavailable_seats = [seat for seat in seat_numbers if seat not in map(str, available_seats)]
        if unavailable_seats:
            return render(request, 'book_ticket.html', {
                'show': show,
                'available_seats': available_seats,
                'error': 'One or more selected seats are unavailable.'
            })

        # Book the tickets for selected seats
        for seat_number in seat_numbers:
            Ticket.objects.create(user=request.user, show=show, seat_number=seat_number)
            send_mail(
            "Ticket confirmation!",
            f"We're pleased to inform you {request.user.username}\nYour Seat is confirmend\nYour seat no is: {seat_number}",
            settings.EMAIL_HOST_USER,
            [request.user.email],
        )

        return redirect('user:shows')

    return render(request, 'book_ticket.html', {
        'show': show,
        'available_seats': available_seats,
        'booked_seats': booked__seats,
        'seat_rows': seat_rows,
        'show_toastr': show_toastr
    })


def login_view(request):
    if request.user.is_authenticated:
            return redirect('user:shows')
    if request.method == "GET":
        return render(request,"login.html")
    cred = request.POST
    username = cred.get("username", "")
    password = cred.get("password", "")
    if not (User.objects.filter(username=username).exists()):
        messages.add_message(request,messages.WARNING,"No user by this username!")
        return redirect("user:login")
    if user := authenticate(request=request, username=username, password=password):
        login(request,user)
        return redirect("user:shows")
    
    messages.add_message(request,messages.ERROR,"Incorrect password!")
    return redirect("user:login")


def sign_up(request):
    if request.user.is_authenticated:
            return redirect('user:shows')

    if request.method=='GET':
        return render(request,"sign_up.html")
    
    cred=request.POST
    username = cred.get("username", "")
    email = cred.get("email", "")
    password = cred.get("password", "")
    confirm = cred.get("confirm_password", "")
    if User.objects.filter(username=username):
        messages.add_message(request,messages.INFO,"User by this name already exists!")
        return redirect('user:sign_up')
    if password!= confirm != '':
        messages.add_message(request,messages.ERROR,"Password don't match up!")
        return redirect('user:sign_up')
        
    user = User.objects.create(username=username)
    user.email=email
    user.set_password(password)
    user.save()
    messages.add_message(request,messages.SUCCESS,"You successfully signed up!")
    
    return redirect("user:login")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('user:login')


# function to input user rating
def submit_rating(request, movie_id):
    if request.method == 'POST':
        user_rating = float(request.POST.get('user_rating'))
        movie = Movies.objects.get(id=movie_id)

        print(f"User Rating: {user_rating}, Movie ID: {movie_id}")  # Debugging line

        # Update user rating and count
        if movie.user_rating is not None:
            movie.user_rating = (movie.user_rating * movie.rating_count + user_rating) / (movie.rating_count + 1)
            movie.rating_count += 1
        else:
            movie.user_rating = user_rating
            movie.rating_count = 1

        movie.save()
        return redirect('user:movie_list')

    return redirect('user:movie_list')  # Handle non-POST requests safely

@method_decorator(login_required, name="dispatch")
class AboutMovie(View):

    template_name="about_movie.html"

    def get(self,request,*args, **kwargs):
        movie_name= request.GET.get('movie_name')
        if not Movies.objects.filter(title=movie_name).exists():
            return render(request,'movie_not_found.html')
        movie= Movies.objects.get(title= movie_name)
        reviews = Reviews.objects.filter(review_of=movie)

        can_review= False
        if Ticket.objects.filter(user=request.user,show__movie=movie).exists():
            ticket = Ticket.objects.get(
                user=request.user, show__movie=movie
            )
            str_time_now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            str_movie_time = ticket.show.time.strftime("%d/%m/%Y, %H:%M:%S")
            time_now = datetime.strptime(str_time_now, "%d/%m/%Y, %H:%M:%S")
            movie_time = datetime.strptime(str_movie_time, "%d/%m/%Y, %H:%M:%S")

            if time_now > movie_time:
                can_review = not can_review

        context = {
            "movie": movie,
            "reviews":reviews,
            'can_review':can_review,
        }
        return render(request,self.template_name ,context=context)

    def post(self,request,*args, **kwargs):
        movie_name=request.POST.get("movie_name")
        review=request.POST.get("review")
        movie=Movies.objects.get(title=movie_name)
        review=profanity.censor(review)

        review=Reviews.objects.create(
            review_content=review,
            review_from=request.user,
            review_of=movie
        )
        review.save()
        url = f"{reverse('user:about_movie')}?{urlencode({'movie_name': movie_name})}"
        return redirect(url)
