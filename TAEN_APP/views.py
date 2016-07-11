from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib import auth
from registration.backends.default.views import ActivationView, RegistrationView
from registration.models import RegistrationManager, RegistrationProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from TAEN_APP.forms import EditProfile, EditUser, RegistrationForm, EditPortfolio
from TAEN_APP.models import Entertaener, Talent, PortfolioLink
import math
from django.db.models import Func, F
import json

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

def paginationPageList(pageRange, currentPage, numPages):
    paginatorList = [(currentPage, True),]

    if ((currentPage - 2) in pageRange):
        paginatorList.append(((currentPage - 2), True))
    elif ((currentPage + 3) in pageRange):
        paginatorList.append(((currentPage + 3), True))
    else:
        paginatorList.append(((currentPage + 3), False))

    if ((currentPage - 1) in pageRange):
        paginatorList.append(((currentPage - 1), True))
    elif ((currentPage + 4) in pageRange):
        paginatorList.append(((currentPage + 4), True))
    else:
        paginatorList.append(((currentPage + 4), False))

    if ((currentPage + 1) in pageRange):
        paginatorList.append(((currentPage + 1), True))
    elif (numPages < 5):
        paginatorList.append(((currentPage + 1), False))
    else:
        paginatorList.append(((currentPage - 4), True))

    if ((currentPage + 2) in pageRange):
        paginatorList.append(((currentPage + 2), True))
    elif (numPages < 5):
        paginatorList.append(((currentPage + 2), False))
    else:
        paginatorList.append(((currentPage - 3), True))

    paginatorList.sort(key=lambda x: x[0])
    return paginatorList

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

    paginator = Paginator(entertaenerList, 16)
    page = request.GET.get('page')
    try:
        entertaeners = paginator.page(page)
    except PageNotAnInteger:
        entertaeners = paginator.page(1)
    except EmptyPage:
        entertaeners = paginator.page(paginator.num_pages)

    paginatorList = paginationPageList(paginator.page_range, entertaeners.number, paginator.num_pages)
    talentList = Talent.objects.all()
    return render(request, 'home.html', {
            'profiles': entertaeners,
            'talents': talentList,
            'pages': paginatorList,
            'currentPage': entertaeners.number})

@login_required
def profile(request, username=None):
    context = {}
    if username != None and username != request.user.username:
        user = User.objects.get(username=username)
        context['distance'] = DistanceBetween(request.user.profile.latitude, request.user.profile.longitude, user.profile.latitude, user.profile.longitude)
        context['isContact'] = request.user.profile.contacts.filter(user=user).exists()
        context['num_contacts'] = user.profile.contacted.count()
    else:
        user = request.user
        context['isSelf'] = True
    context['profile'] = user.profile
    return render(request, 'profile.html', context)

@login_required
def profileEdit(request):
    if request.method == 'POST':
        profileForm = EditProfile(request.POST, request.FILES or None, instance=request.user.profile)
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
                'longitude': request.user.profile.longitude,
                'equipment': request.user.profile.equipment,
                'specialization': request.user.profile.specialization
        }
        userData = {
                'email': request.user.email,
        }
        profileForm = EditProfile(initial=profileData)
        userForm = EditUser(initial=userData)

    return render(request, 'profileEdit.html', {
        'profileForm': profileForm,
        'userForm': userForm,
        'portfolioLinks': request.user.profile.portfolioLink})

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
def removeContact(request, username):
    if username == None or username == request.user.username:
        return Http404("Error cannot add contact without username")
    else:
        userToRemove = User.objects.get(username=username)
        userToRemove = Entertaener.objects.get(user=userToRemove)
        request.user.profile.contacts.remove(userToRemove)
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

    paginator = Paginator(entertaenerList, 16)
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

def login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me'):
            request.session.set_expiry(0)
    return auth.views.login(request, *args, **kwargs)

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

@login_required
@require_POST
def updatePortfolio(request):
    if request.method == 'POST':
        deletedLinks = request.POST.getlist('deleted')
        numberOfLinksToAdd = request.POST.get('numberOfLinksToAdd')
        newLinks = request.POST.getlist('newLinks')
        if deletedLinks and len(deletedLinks):
            for link in deletedLinks:
                # exclude last index in string because the url is often stored without a back-slash
                portfolioObject = request.user.profile.portfolioLink.filter(link__icontains=link[:-1])
                portfolioObject.delete()
        if numberOfLinksToAdd and newLinks and numberOfLinksToAdd > 1:
            for link in newLinks:
                link = urlValidation(link)
                if link:
                    newLinkObject = PortfolioLink(link=link, entertaener=request.user.profile)
                    newLinkObject.save()

        responseData = {}
        responseData['results'] = 'success'
        return HttpResponse(
                json.dumps(responseData),
                content_type = 'application/json'
        )
    else:
        return HttpResponse(
                json.dumps({'error': 'an error has occurred'}),
                content_type = 'application/json'
        )

def urlValidation(url):
    if (len(url) > 23) and ((url[:24] == 'https://www.youtube.com/') or (url[:23] == 'http://www.youtube.com/')):
        return url
    elif (len(url) > 15) and (url[:16] == 'www.youtube.com/'):
        return 'https://' + url
    elif (len(url) > 11) and (url[:12] == 'youtube.com/'):
        return 'https://www.' + url
