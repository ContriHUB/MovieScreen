from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import submit_rating

from .views import shows,add_movie,AddShowView,MovieAutocomplete,movie_list,book_ticket,login_view,sign_up,logout_view,movie_details

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('shows/', shows, name='shows'),
    path('movie_list/',movie_list, name='movie_list'),
    path('add_movie/', add_movie, name='add_movie'),
    path('add_show/', AddShowView.as_view(), name='AddShowView'),
    path('book_ticket/<int:show_id>/', book_ticket, name='book_ticket'),
    path('autocomplete/', MovieAutocomplete.as_view(), name='movie_autocomplete'),
    path('login/',login_view,name='login'),
    path('sign_up/',sign_up,name='sign_up'),
    path('logout/',logout_view,name='logout'),
    path('movie_details/',movie_details,name='movie_details'),
    path('submit_rating/<int:movie_id>/', submit_rating, name='submit_rating')
]
