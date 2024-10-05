from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import shows,add_movie,movie_list,AddShowView
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('shows/', shows, name='shows'),
    path('add_movie/', add_movie, name='add_movie'),
    path('movie_list/', movie_list, name='movie_list'),
    path('add_show/', AddShowView.as_view(), name='AddShowView'),
    
    
]