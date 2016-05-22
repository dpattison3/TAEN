from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

@login_required
def profiles(request):
    return render(request, 'profile.html', {})
