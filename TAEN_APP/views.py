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
from TAEN_APP.forms import EditProfile, EditUser, RegistrationForm, EditProject, EditTool
from TAEN_APP.models import Entertaener, Talent, PortfolioLink, Project, Tool
import math
from django.db.models import Func, F
import json
import re

# list of urls allowed for portfolio links uploaded by users - prevents spam/malicious sites
url_whitelist = [
        re.compile('https://www.youtube.com/.*'),
        re.compile('http://www.youtube.com/.*'),
        re.compile('www.youtube.com/.*'),
        re.compile('youtube.com/.*'),
        re.compile('https://soundcloud.com/.*'),
        re.compile('http://soundcloud.com/.*'),
        re.compile('https://www.soundcloud.com/.*'),
        re.compile('http://www.soundcloud.com/.*'),
        re.compile('www.soundcloud.com/.*'),
        re.compile('soundcloud.com/.*'),
        re.compile('https://www.spotify.com/.*'),
        re.compile('https://www.spotify.com/.*'),
        re.compile('www.spotify.com/.*'),
        re.compile('spotify.com/.*'),
        re.compile('http://www.apple.com/music/.*'),
        re.compile('https://www.apple.com/music/.*'),
        re.compile('www.apple.com/music/.*'),
        re.compile('apple.com/music/.*'),
        re.compile('https://twitter.com/.*'),
        re.compile('http://twitter.com/.*'),
        re.compile('https://www.twitter.com/.*'),
        re.compile('http://www.twitter.com/.*'),
        re.compile('www.twitter.com/.*'),
        re.compile('twitter.com/.*'),
        re.compile('https://www.facebook.com/.*'),
        re.compile('http://www.facebook.com/.*'),
        re.compile('https://facebook.com/.*'),
        re.compile('https://facebook.com/.*'),
        re.compile('www.facebook.com/.*'),
        re.compile('facebook.com/.*'),
        re.compile('https://www.pinterest.com/.*'),
        re.compile('http://www.pinterest.com/.*'),
        re.compile('https://pinterest.com/.*'),
        re.compile('http://pinterest.com/.*'),
        re.compile('www.pinterest.com/.*'),
        re.compile('pinterest.com/.*'),
        re.compile('https://www.tumblr.com/.*'),
        re.compile('https://www.tumblr.com/.*'),
        re.compile('https://tumblr.com/.*'),
        re.compile('http://tumblr.com/.*'),
        re.compile('www.tumblr.com/.*'),
        re.compile('tumblr.com/.*'),
        re.compile('https://www.instagram.com/.*'),
        re.compile('http://www.instagram.com/.*'),
        re.compile('https://instagram.com/.*'),
        re.compile('http://instagram.com/.*'),
        re.compile('www.instagram.com/.*'),
        re.compile('instagram.com/.*'),
]

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

def termsOfService(request):
    return render(request, 'termsOfService.html', {})

@login_required
def home(request):
    distanceCalculation = DistanceBetweenObjects(request.user.profile.latitude, request.user.profile.longitude)
    entertaenerList = Entertaener.objects.exclude(user__is_active=False).exclude(user=request.user).annotate(distance=distanceCalculation).order_by('distance')

    search = request.GET.get('search')
    talentFilter = request.GET.get('filter')
    if talentFilter:
        talentObj = Talent.objects.get(talent=(Talent.Talent_Dictionary[talentFilter]))
        entertaenerList = entertaenerList.filter(talent=talentObj)
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
        profileData = {
                'name': request.user.profile.name,
                'gender': request.user.profile.gender,
                'pitch': request.user.profile.pitch,
                'picture': request.user.profile.picture,
                'talent': request.user.profile.talent.all(),
                'latitude': request.user.profile.latitude,
                'longitude': request.user.profile.longitude,
                'city': request.user.profile.city,
                'state': request.user.profile.state,
                'genres': request.user.profile.genres,
                'age': request.user.profile.age,
        }
        userData = {
                'email': request.user.email,
        }
        profileForm = EditProfile(initial=profileData)
        userForm = EditUser(initial=userData)

    context = {
            'profileForm': profileForm,
            'currentPorfilePicture': request.user.profile.picture,
            'userForm': userForm,
            'portfolioLinks': request.user.profile.portfolioLink.all(),
            'projects': request.user.profile.project.all(),
            'tools': request.user.profile.tool.all(),
    }
    return render(request, 'profileEdit.html', context)

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
        talentObj = Talent.objects.get(talent=(Talent.Talent_Dictionary[talentFilter]))
        entertaenerList = entertaenerList.filter(talent=talentObj)
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
        titles = request.POST.getlist('titles')
        if deletedLinks and len(deletedLinks):
            for link in deletedLinks:
                # exclude last index in string because the url is often stored without a back-slash
                portfolioObject = request.user.profile.portfolioLink.filter(link__icontains=link[:-1])
                portfolioObject.delete()
        if numberOfLinksToAdd and newLinks and numberOfLinksToAdd > 1:
            for link, title in zip(newLinks, titles):
                link = urlValidation(link)
                if link and (title != None or title != ''):
                    newLinkObject = PortfolioLink(link=link, entertaener=request.user.profile, title=title)
                    newLinkObject.save()
                elif link:
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
    if any(regex.match(url) for regex in url_whitelist):
        return url

@login_required
def addProject(request):
    if request.method == 'POST':
        projectForm = EditProject(request.POST, request.FILES or None)
        valid = projectForm.is_valid()
        if valid:
            link = projectForm.cleaned_data['link']
            linkValid = urlValidation(link)
        else:
            linkValid = True
        if valid and linkValid:
            project = projectForm.save(commit=False)
            project.entertaener = request.user.profile
            project.save()
            return redirect('edit_profile')
    else:
        projectForm = EditProject()
    return render(request, 'projectEdit.html', {'projectForm': projectForm})


@login_required
def editProject(request, projectId):
    project = get_object_or_404(Project, pk=projectId)

    if request.method == 'POST':
        projectForm = EditProject(request.POST, request.FILES or None, instance=project)
        valid = projectForm.is_valid()
        if valid:
            link = projectForm.cleaned_data['link']
            linkValid = urlValidation(link)
        else:
            linkValid = True
        if valid and linkValid:
            projectForm.save(commit=True)
            return redirect('edit_profile')
    else:
        projectData = {
                'title': project.title,
                'contributors': project.contributors,
                'description': project.description,
                'link': project.link,
                'image': project.image,
        }
        projectForm = EditProject(initial=projectData)
    return render(request, 'projectEdit.html', {
            'projectForm': projectForm,
            'project': project
    })

@login_required
def deleteProject(request, projectId):
    project = get_object_or_404(Project, pk=projectId)
    project.delete()
    return redirect('edit_profile')

@login_required
def addTool(request):
    if request.method == 'POST':
        toolForm = EditTool(request.POST, request.FILES or None)
        if toolForm.is_valid():
            tool = toolForm.save(commit=False)
            tool.entertaener = request.user.profile
            tool.save()
            return redirect('edit_profile')
    else:
        toolForm = EditTool()
    return render(request, 'toolEdit.html', {'toolForm': toolForm})

@login_required
def editTool(request, toolId):
    tool = get_object_or_404(Tool, pk=toolId)

    if request.method == 'POST':
        toolForm = EditTool(request.POST, request.FILES or None, instance=tool)
        if toolForm.is_valid():
            toolForm.save(commit=True)
            return redirect('edit_profile')
    else:
        toolData = {
                'title': tool.title,
                'description': tool.description,
                'image': tool.image,
        }
        toolForm = EditTool(initial=toolData)
    return render(request, 'toolEdit.html', {
            'toolForm': toolForm,
            'tool': tool,
    })

@login_required
def deleteTool(request, toolId):
    tool = get_object_or_404(Tool, pk=toolId)
    tool.delete()
    return redirect('edit_profile')
