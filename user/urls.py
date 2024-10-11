from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from .views import shows,add_movie,AddShowView,MovieAutocomplete,movie_list,book_ticket,movie_review

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('shows/', shows, name='shows'),
    path('movie_list/',movie_list, name='movie_list'),
    path('add_movie/', add_movie, name='add_movie'),
    path('add_show/', AddShowView.as_view(), name='AddShowView'),
    path('book_ticket/<int:show_id>/', book_ticket, name='book_ticket'),
    path('autocomplete/', MovieAutocomplete.as_view(), name='movie_autocomplete'),
    path('review/<int:movie_id>/', movie_review, name='movie_review'),
    
]
