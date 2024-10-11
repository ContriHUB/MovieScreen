from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Show,UserRating

class ShowForm(forms.ModelForm):
    class Meta:
        model = Show
        fields = ['movie', 'time', 'uuid']

class UserRatingForm(forms.ModelForm):
    class Meta:
        model = UserRating 
        fields = ['stars'] 

      
        widgets = {
            'stars': forms.NumberInput(attrs={
                'type': 'range',
                'min': '0',
                'max': '5',
                'step': '0.5',
                'value': '2.5',  
                'oninput': "document.getElementById('ratingValue').innerText = this.value"
            }),
        }