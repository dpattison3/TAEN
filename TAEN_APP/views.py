from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from TAEN_APP.forms import EditProfile
from TAEN_APP.models import Entertaener, Talent

def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

@login_required
def home(request):
    entries = Entertaener.objects.all()
    return render(request, 'home.html', {'profiles': entries})

@login_required
def profile(request):
    return render(request, 'profile.html', {'profile': request.user.profile})

@login_required
def profileEdit(request):
    if request.method == 'POST':
        form = EditProfile(request.POST,request.FILES or None, instance=request.user.profile)

        if form.is_valid():
            form.save(commit=True)
            return profile(request)
        else:
            print form.errors
    else:
        data = {'name': request.user.profile.name,
                'pitch': request.user.profile.pitch,
                'picture': request.user.profile.picture,
                #'talent': request.user.profile.talent, TODO preselect existing talents
        }
        form = EditProfile(initial=data)

    return render(request, 'profileEdit.html', {'form': form})

