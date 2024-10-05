from django.db import models

class Movies(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    poster = models.ImageField(upload_to='movie_posters/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Show(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    time = models.DateTimeField()
    uuid = models.CharField(max_length=32, unique=True)
    

    def __str__(self):
     return f"{self.movie.title} ({self.time.strftime('%Y-%m-%d %H:%M')})"

    

    

