from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import shows,add_movie,AddShowView,home,MovieListView
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('shows/', shows, name='shows'),
    path('movie_list/',MovieListView.as_view(), name='movie_list'),
    path('add_movie/', add_movie, name='add_movie'),
    path('add_show/', AddShowView.as_view(), name='AddShowView'),
    
    
]