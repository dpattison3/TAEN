from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from TAEN_APP.forms import EditProfile
from TAEN_APP.models import Entertaener, Talent

def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

@login_required
def home(request):
    entertaenerList = Entertaener.objects.exclude(user=request.user)
    search = request.GET.get('search')
    talentFilter = request.GET.get('filter')
    if talentFilter:
        entertaenerList =  entertaenerList.filter(talent=(Talent.Talent_Dictionary[talentFilter]+1))
    if search:
        entertaenerList = entertaenerList.filter(name__icontains=search).distinct()

    paginator = Paginator(entertaenerList, 3) # show 3 per page
    page = request.GET.get('page')
    try:
        entertaeners = paginator.page(page)
    except PageNotAnInteger:
        entertaeners = paginator.page(1)
    except EmptyPage:
        entertaeners = paginator.page(paginator.num_pages)

    talentList = Talent.objects.all()
    return render(request, 'home.html', {'profiles': entertaeners, 'talents': talentList})

@login_required
def profile(request, username=None):
    if username != None and username != request.user.username:
        user = User.objects.get(username=username)
        isSelf = False
        isContact = request.user.profile.contacts.filter(user=user).exists()
    else:
        user = request.user
        isSelf = True
        isContact = False
    context = {
            'profile': user.profile,
            'isSelf': isSelf,
            'isContact': isContact,
            'contacts': request.user.profile.contacts,
    }
    return render(request, 'profile.html', context)

@login_required
def profileEdit(request):
    if request.method == 'POST':
        form = EditProfile(request.POST,request.FILES or None, instance=request.user.profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', username=request.user.username)
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

@login_required
def addContact(request, username):
    if username == None:
        return Http404("Error cannot add contact without username")
    else:
        userToAdd = User.objects.get(username=username)
        userToAdd = Entertaener.objects.get(user=userToAdd)
        request.user.profile.contacts.add(userToAdd)
        return redirect('profile', username=username)

@login_required
def contacts(request):
    entertaenerList = request.user.profile.contacts.all()

    search = request.GET.get('search')
    talentFilter = request.GET.get('filter')
    if talentFilter:
        entertaenerList =  entertaenerList.filter(talent=(Talent.Talent_Dictionary[talentFilter]+1))
    if search:
        entertaenerList = entertaenerList.filter(name__icontains=search).distinct()

    paginator = Paginator(entertaenerList, 3) # show 3 per page
    page = request.GET.get('page')
    try:
        entertaeners = paginator.page(page)
    except PageNotAnInteger:
        entertaeners = paginator.page(1)
    except EmptyPage:
        entertaeners = paginator.page(paginator.num_pages)

    talentList = Talent.objects.all()
    return render(request, 'home.html', {'profiles': entertaeners, 'talents': talentList})

