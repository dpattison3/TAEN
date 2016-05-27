from django.conf.urls import url, patterns
from django.conf import settings

from . import views

urlpatterns = [
        url(r'^$', views.index, name = 'index'),
        url(r'^about/$', views.about, name = 'about'),
        url(r'^home/$', views.home, name = 'home'),
        url(r'^profile/$', views.profile, name = 'profile'),
        url(r'^edit_profile/$', views.profileEdit, name='edit_profile'),
]
