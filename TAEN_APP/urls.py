from django.conf.urls import url, patterns
from django.contrib.auth.views import password_reset_confirm, password_change #password_reset, password_change
from django.conf import settings
from . import views

urlpatterns = [
        url(r'^$', views.index, name = 'index'),
        url(r'^about/$', views.about, name = 'about'),
        url(r'^home/$', views.home, name = 'home'),
        url(r'^edit_profile/$', views.profileEdit, name='edit_profile'),
        url(r'^profile/$', views.profile, name='profileSelf'),
        url(r'^profile/(?P<username>[\w.@+-]+)/$', views.profile, name='profile'),
        url(r'^profile/(?P<username>[\w.@+-]+)/add_contact/$', views.addContact, name='add_contact'),
        url(r'^profile/(?P<username>[\w.@+-]+)/remove_contact/$', views.removeContact, name='remove_contact'),
        url(r'^contacts/$', views.contacts, name='contacts'),
        url(r'^accounts/activate/(?P<activation_key>\w+)/$', views.ActivateAccount.as_view(), name='activate'),
        url(r'^accounts/register/$', views.Register.as_view(), name='register'),
        url(r'^accounts/register/complete/$', views.registrationComplete, name='registration_complete'),
        url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'post_reset_redirect': '/accounts/login/'}),
        url(r'^accounts/password/change/$', password_change, {'post_change_redirect': '/home/'}, name='password_change'),
        url(r'^termsOfService/$', views.termsOfService, name='termsOfService'),
]
