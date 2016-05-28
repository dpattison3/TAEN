from django import forms
from .models import Entertaener

class EditProfile(forms.ModelForm):
    name = forms.CharField(max_length = 32, help_text = "Name")
    pitch = forms.CharField(max_length=5000, help_text = "Pitch")
    portfolio = forms.URLField(help_text = "Portfolio link", required=False)
    picture = forms.ImageField(required=False)
    
    class Meta:
        model = Entertaener
        fields = ['name', 'pitch', 'portfolio', 'picture']

