from django.shortcuts import render, redirect
from .models import Show, Movies, Ticket
from django.utils import timezone
from .forms import ShowForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Count

def shows(request):
    upcoming_shows = Show.objects.all().order_by('-time')
    return render(request, 'shows.html', {'shows': upcoming_shows})

def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        poster = request.FILES.get('poster')
        available = request.POST.get('available', False)
        movie = Movies.objects.create(title=title, description=description, poster=poster, available=available)
        movie.save()
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

@login_required
def book_ticket(request, show_id):
    show = Show.objects.get(id=show_id)

   
    booked_seats = Ticket.objects.filter(show=show).values_list('seat_number', flat=True)

   
    total_seats = range(1, 101) 


    available_seats = [seat for seat in total_seats if seat not in booked_seats]

    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')

       
        ticket_count = Ticket.objects.filter(
            user=request.user,
            booked_at__month=timezone.now().month,
            booked_at__year=timezone.now().year
        ).count()

        if ticket_count >= 2:
            return render(request, 'book_ticket.html', {'show': show, 'available_seats': available_seats, 'error': 'You can only book up to 2 tickets per month.'})

        if seat_number not in map(str, available_seats):
            return render(request, 'book_ticket.html', {'show': show, 'available_seats': available_seats, 'error': 'This seat is already booked or unavailable.'})

       
        Ticket.objects.create(user=request.user, show=show, seat_number=seat_number)
        return redirect('user:shows')

    return render(request, 'book_ticket.html', {'show': show, 'available_seats': available_seats})
