from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail
from .models import Entertaener, Talent, PortfolioLink

class EditProfile(forms.ModelForm):
    name = forms.CharField(help_text='Name:', required=False)
    pitch = forms.CharField(help_text='Pitch:', required=False)
    age = forms.IntegerField(help_text='Age:', required=False)
    gender = forms.CharField(help_text='Gender:', required=False)
    talent = forms.ModelMultipleChoiceField(queryset=Talent.objects.all(), widget=forms.CheckboxSelectMultiple, help_text='Talents:', required=False)
    picture = forms.ImageField(help_text='Profile picture:', required=False)
    latitude = forms.FloatField(help_text='latitude', required=False)
    longitude = forms.FloatField(help_text='longitude', required=False)
    city = forms.CharField(help_text='city', required=False)
    state = forms.CharField(help_text='state', required=False)
    genres = forms.CharField(help_text='genres', required=False)

    class Meta:
        model = Entertaener
        fields = ['name', 'pitch', 'age', 'picture', 'talent', 'latitude', 'longitude', 'city', 'state', 'genres', 'gender']

class EditUser(forms.ModelForm):
    email = forms.EmailField(help_text='Email:', required=False)
    class Meta:
        model = User
        fields = ['email']

class RegistrationForm(RegistrationFormTermsOfService, RegistrationFormUniqueEmail):
    pass
