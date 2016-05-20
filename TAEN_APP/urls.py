from django.conf.urls import url, patterns
from django.conf import settings

from . import views

urlpatterns = [
        url(r'^$', views.home, name = 'home'),
        url(r'^about/$', views.about, name = 'about'),
        url(r'^profiles/$', views.profiles, name = 'profile views'),
]

if settings.DEBUG:
    urlpatterns += patterns(
            'django.views.static',
            (r'^media/(?P<path>.*)',
            'serve',
            {'document_root': settings.MEDIA_ROOT}), )
