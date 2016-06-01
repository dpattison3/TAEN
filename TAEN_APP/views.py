from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from TAEN_APP.forms import EditProfile
from TAEN_APP.models import Entertaener, Talent

def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

@login_required
def home(request):
    entertaenerList = Entertaener.objects.exclude(user=request.user)
    paginator = Paginator(entertaenerList, 1) # show 3 per page

    page = request.GET.get('page')
    try:
        entertaeners = paginator.page(page)
    except PageNotAnInteger:
        entertaeners = paginator.page(1)
    except EmptyPage:
        entertaeners = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'profiles': entertaeners})

@login_required
def profile(request, username=None):
    if username != None and username != request.user.username:
        user = User.objects.get(username=username)
        isSelf = False
        isContact = False
    else:
        user = request.user
        isSelf = True
        isContact = False
    context = {
            'profile': user.profile,
            'isSelf': isSelf,
            'isContact': isContact
    }
    return render(request, 'profile.html', context)

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

