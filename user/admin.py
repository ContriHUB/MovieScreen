from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Movies,Show,Ticket,Reviews
from .models import Tag, Movies

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Movies)

admin.site.register(Show)
admin.site.register(Ticket)
admin.site.register(Reviews)
