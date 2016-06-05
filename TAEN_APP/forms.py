from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail
from .models import Entertaener, Talent

class EditProfile(forms.ModelForm):
    name = forms.CharField(help_text= "Name:", required=False)
    pitch = forms.CharField(help_text="Pitch:", required=False)
    portfolio = forms.URLField(help_text="Portfolio link:", required=False)
    talent = forms.ModelMultipleChoiceField(queryset=Talent.objects.all(), widget=forms.CheckboxSelectMultiple, help_text='Talents:', required=False)
    picture = forms.ImageField(help_text='Profile picture:', required=False)
    
    class Meta:
        model = Entertaener
        fields = ['name', 'pitch', 'portfolio', 'picture', 'talent']

class EditUser(forms.ModelForm):
    email = forms.EmailField(help_text='Email:', required=False)
    class Meta:
        model = User
        fields = ['email']

class RegistrationForm(RegistrationFormTermsOfService, RegistrationFormUniqueEmail):
    pass
