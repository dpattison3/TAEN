from django import forms
from .models import Entertaener

class EditProfile(forms.ModelForm):
    name = forms.CharField(max_length = 32, help_text = "what is help text")
    
    class Meta:
        model = Entertaener
        fields = ['name',] # 'industry', 'pitch', 'portfolio']

