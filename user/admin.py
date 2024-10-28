from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Movies,Show,Ticket,Reviews

admin.site.register(Movies)

admin.site.register(Show)
admin.site.register(Ticket)
admin.site.register(Reviews)
