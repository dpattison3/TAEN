from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from registration.backends.default.views import ActivationView, RegistrationView
from registration.models import RegistrationManager, RegistrationProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from TAEN_APP.forms import EditProfile, EditUser, RegistrationForm
from TAEN_APP.models import Entertaener, Talent
import math
from django.db.models import Func, F

# functions used for calculating the distances between users using database level functions
class Sin(Func):
    function = 'SIN'
class Cos(Func):
    function = 'COS'
class Acos(Func):
    function = 'ACOS'
class Radians(Func):
    function = 'RADIANS'
class Round(Func):
    function = 'ROUND'
# function for calculating the distances between users - used for databse objects
def DistanceBetweenObjects(referenceLat, referenceLon):
    radlat = Radians(referenceLat)
    radlong = Radians(referenceLon)
    radflat = Radians(F('latitude'))
    radflong = Radians(F('longitude'))
    return Round(3959.0 * Acos(Cos(radlat) * Cos(radflat) * Cos(radflong - radlong) + Sin(radlat) * Sin(radflat)))
# function for calculating the distances between users - used for single object with relevant values extracted
def DistanceBetween(referenceLat, referenceLong, compLat, compLon):
    radlat = math.radians(referenceLat)
    radlong = math.radians(referenceLong)
    radflat = math.radians(compLat)
    radflong = math.radians(compLon)
    return math.floor(3959.0 * math.acos(math.cos(radlat) * math.cos(radflat) * math.cos(radflong - radlong) + math.sin(radlat) * math.sin(radflat)))

def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

def termsOfService(request):
    return render(request, 'termsOfService.html', {})

@login_required
def home(request):
    distanceCalculation = DistanceBetweenObjects(request.user.profile.latitude, request.user.profile.longitude)
    entertaenerList = Entertaener.objects.exclude(user=request.user).annotate(distance=distanceCalculation).order_by('distance')

    search = request.GET.get('search')
    talentFilter = request.GET.get('filter')
    if talentFilter:
        entertaenerList =  entertaenerList.filter(talent=(Talent.Talent_Dictionary[talentFilter]+1))
    if search:
        entertaenerList = entertaenerList.filter(name__icontains=search).distinct()

    paginator = Paginator(entertaenerList, 3)
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
    context = {}
    if username != None and username != request.user.username:
        user = User.objects.get(username=username)
        context['distance'] = DistanceBetween(request.user.profile.latitude, request.user.profile.longitude, user.profile.latitude, user.profile.longitude)
        context['isContact'] = request.user.profile.contacts.filter(user=user).exists()
    else:
        user = request.user
        context['contacts'] = request.user.profile.contacts
        context['isSelf'] = True
    context['profile'] = user.profile
    return render(request, 'profile.html', context)

@login_required
def profileEdit(request):
    if request.method == 'POST':
        profileForm = EditProfile(request.POST,request.FILES or None, instance=request.user.profile)
        userForm = EditUser(request.POST, instance=request.user)

        if profileForm.is_valid() and userForm.is_valid():
            profileForm.save(commit=True)
            userForm.save(commit=True)
            return redirect('profile', username=request.user.username)
        else:
            print(profileForm.errors)
            print(userForm.errors)
    else:
        profileData = {
                'name': request.user.profile.name,
                'pitch': request.user.profile.pitch,
                'picture': request.user.profile.picture,
                'talent': request.user.profile.talent.all(),
                'latitude': request.user.profile.latitude,
                'longitude': request.user.profile.longitude
        }
        userData = {
                'email': request.user.email,
        }
        profileForm = EditProfile(initial=profileData) #, prefix='pro')
        userForm = EditUser(initial=userData) #, prefix='usr')

    return render(request, 'profileEdit.html', {'profileForm': profileForm, 'userForm': userForm})

@login_required
def addContact(request, username):
    if username == None or username == request.user.username:
        return Http404("Error cannot add contact without username")
    else:
        userToAdd = User.objects.get(username=username)
        userToAdd = Entertaener.objects.get(user=userToAdd)
        request.user.profile.contacts.add(userToAdd)
        return redirect('profile', username=username)

@login_required
def contacts(request):
    distanceCalculation = DistanceBetweenObjects(request.user.profile.latitude, request.user.profile.longitude)
    entertaenerList = request.user.profile.contacts.all().annotate(distance=distanceCalculation).order_by('distance')

    search = request.GET.get('search')
    talentFilter = request.GET.get('filter')
    if talentFilter:
        entertaenerList =  entertaenerList.filter(talent=(Talent.Talent_Dictionary[talentFilter]+1))
    if search:
        entertaenerList = entertaenerList.filter(name__icontains=search).distinct()

    paginator = Paginator(entertaenerList, 3)
    page = request.GET.get('page')
    try:
        entertaeners = paginator.page(page)
    except PageNotAnInteger:
        entertaeners = paginator.page(1)
    except EmptyPage:
        entertaeners = paginator.page(paginator.num_pages)

    talentList = Talent.objects.all()
    return render(request, 'home.html', {'profiles': entertaeners, 'talents': talentList})

class ActivateAccount(ActivationView):
    def get_success_url(self, user):
        return '/profile/'

class Register(RegistrationView):
    form_class = RegistrationForm

def registrationComplete(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
    if request.method != 'POST' or (not email and not (email and username)):
        return render(request, 'registration_complete.html')
    site = get_current_site(request)
    try:
        if email and not username:
            user = User.objects.get(email=email)
        elif email and username:
            user = User.objects.get(username=username)
            user.email = email
            user.save()
        registrationProfile = RegistrationProfile.objects.get(user=user)
        if not registrationProfile.activated and not registrationProfile.activation_key_expired():
            registrationProfile.create_new_activation_key()
            registrationProfile.send_activation_email(site, request)
    except ObjectDoesNotExist:
        pass
    return redirect('registration_complete')
