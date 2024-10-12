from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import shows, add_movie, movie_list, AddShowView,MovieAutocomplete, redirect_to_shows

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirect root URL to /shows/
     path('', redirect_to_shows, name='redirect_to_shows'),

    path('shows/', shows, name='shows'),
    path('add_movie/', add_movie, name='add_movie'),
    path('movie_list/', movie_list, name='movie_list'),
    path('add_show/', AddShowView.as_view(), name='add_show_view'),
    path('autocomplete/', MovieAutocomplete.as_view(), name='movie_autocomplete'),
]
