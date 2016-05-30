from django import forms
from .models import Entertaener, Talent

class EditProfile(forms.ModelForm):
    name = forms.CharField(help_text= "Name:", required=False)
    pitch = forms.CharField(help_text="Pitch:", required=False)
    portfolio = forms.URLField(help_text="Portfolio link:", required=False)
    talent = forms.ModelMultipleChoiceField(queryset=Talent.objects.all(), widget=forms.CheckboxSelectMultiple, help_text='Talents:', required=False)
    picture = forms.ImageField(required=False)
    
    class Meta:
        model = Entertaener
        fields = ['name', 'pitch', 'portfolio', 'picture', 'talent']

