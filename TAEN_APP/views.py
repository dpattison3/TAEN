from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from TAEN_APP.forms import EditProfile
from TAEN_APP.models import Entertaener

def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

@login_required
def home(request):
    entry = Entertaener.objects.all()
    return render(request, 'home.html', {'profiles': entry})

@login_required
def profile(request):
    return render(request, 'profile.html', {'profile': request.user.profile})

@login_required
def profileEdit(request):
    if request.method == 'POST':
        data = {'name': request.user.profile.name}
        form = EditProfile(request.POST, initial = data, instance=request.user.profile)

        if form.is_valid():
            form.save(commit = True)
            return home(request)
        else:
            print form.errors
    else:
        form = EditProfile()

    return render(request, 'profileEdit.html', {'form': form})
