from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Industry(models.Model):
    Film = 'F'
    Photography = 'P'
    Music = 'M'
    Industry_Choices = (
            (Film, 'Film'),
            (Photography, 'Photography'),
            (Music, 'Music'),
    )
    industry = models.CharField(max_length=1, choices=Industry_Choices, blank=True)

    def __str__(self):
        return industry

class Entertaener(models.Model):
    # user = models.OneToOneField(User)
    name = models.CharField(max_length = 32, default='anonymous');

    industry = models.ForeignKey(Industry, null=True)

    pitch = models.CharField(max_length=5000, blank=True)

    portfolio = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
