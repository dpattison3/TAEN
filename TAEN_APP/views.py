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


def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

def termsOfService(request):
    return render(request, 'termsOfService.html', {})

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
        }
        userData = {
                'email': request.user.email,
        }
        profileForm = EditProfile(initial=profileData) #, prefix='pro')
        userForm = EditUser(initial=userData) #, prefix='usr')

    return render(request, 'profileEdit.html', {'profileForm': profileForm, 'userForm': userForm})

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

class ActivateAccount(ActivationView):
    def get_success_url(self, user):
        return '/profile/'

class Register(RegistrationView):
    form_class = RegistrationForm

def registrationComplete(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            site = get_current_site(request)
            try:
                user = User.objects.get(email=email)
                regprof = RegistrationProfile.objects.get(user=user)
                if not regprof.activated and not regprof.activation_key_expired():
                    regprof.create_new_activation_key()
                    regprof.send_activation_email(site, request)
            except ObjectDoesNotExist:
                pass
            return redirect('registration_complete')
    return render(request, 'registration_complete.html')
