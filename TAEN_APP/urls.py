from django.conf.urls import url, patterns
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
        url(r'contacts/$', views.contacts, name='contacts'),
]
