from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail
from .models import Entertaener, Talent, PortfolioLink

class EditProfile(forms.ModelForm):
    name = forms.CharField(help_text= "Name:", required=False)
    pitch = forms.CharField(help_text="Pitch:", required=False)
    talent = forms.ModelMultipleChoiceField(queryset=Talent.objects.all(), widget=forms.CheckboxSelectMultiple, help_text='Talents:', required=False)
    picture = forms.ImageField(help_text='Profile picture:', required=False)
    latitude = forms.FloatField(help_text='latitude', required=False)
    longitude = forms.FloatField(help_text='longitude', required=False)

    class Meta:
        model = Entertaener
        fields = ['name', 'pitch', 'picture', 'talent', 'latitude', 'longitude']

class EditUser(forms.ModelForm):
    email = forms.EmailField(help_text='Email:', required=False)
    class Meta:
        model = User
        fields = ['email']

class RegistrationForm(RegistrationFormTermsOfService, RegistrationFormUniqueEmail):
    pass

class EditPortfolio(forms.ModelForm):
    entertaener = forms.ModelChoiceField(queryset=Entertaener.objects.all(), widget=forms.HiddenInput(), required=False)
    class Meta:
        model = PortfolioLink
        fields = ['entertaener', 'link']
