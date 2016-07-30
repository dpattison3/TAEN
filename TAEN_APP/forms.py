from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail
from .models import Entertaener, Talent, Project, Tool

class EditProfile(forms.ModelForm):
    name = forms.CharField(required=False)
    pitch = forms.CharField(required=False)
    age = forms.IntegerField(required=False)
    gender = forms.CharField(required=False)
    talent = forms.ModelMultipleChoiceField(queryset=Talent.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    picture = forms.ImageField(required=False)
    latitude = forms.FloatField(required=False)
    longitude = forms.FloatField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    genres = forms.CharField(required=False)

    class Meta:
        model = Entertaener
        fields = ['name', 'pitch', 'age', 'picture', 'talent', 'latitude', 'longitude', 'city', 'state', 'genres', 'gender']

class EditUser(forms.ModelForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ['email']

class EditProject(forms.ModelForm):
    title = forms.CharField(max_length=32, required=True)
    contributors = forms.CharField(max_length=259, required=False)
    description = forms.CharField(max_length=2500, required=False)
    link = forms.URLField(required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Project
        fields = ['title', 'contributors', 'description', 'link', 'image',]

class EditTool(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(max_length=300, required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Tool
        fields = ['title', 'description', 'image',]

class RegistrationForm(RegistrationFormTermsOfService, RegistrationFormUniqueEmail):
    pass
