from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Movies(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    poster = models.ImageField(upload_to='movie_posters/')
    available = models.BooleanField(default=True)
    stars = models.FloatField(null=True, blank=True)
    

    def __str__(self):
        return self.title


class UserRating(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='user_ratings') 
    stars = models.FloatField() 
    created_at = models.DateTimeField(auto_now_add=True)

    
class Show(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    time = models.DateTimeField()
    uuid = models.CharField(max_length=32, unique=True)
    

    def __str__(self):
        return f"{self.movie.title} ({self.time.strftime('%Y-%m-%d %H:%M')})"


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)  # e.g., "A1", "B2"
    booked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'show', 'seat_number')  # Ensure no duplicate bookings for the same seat

    def __str__(self):
        return f"{self.user.username} - {self.show.movie.title} - Seat: {self.seat_number}"