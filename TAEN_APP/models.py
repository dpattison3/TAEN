from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os

def imgUploadLocation(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Talent(models.Model):
    Recording = 0
    Artist = 1
    Producer = 2
    Mixer = 3
    Talent_Choices = [
            (Recording, 'Recording'),
            (Artist, 'Artist'),
            (Producer, 'Producer'),
            (Mixer, 'Mixer'),
    ]
    Talent_Dictionary = {
            'Recording': Recording,
            'Artist': Artist,
            'Producer': Producer,
            'Mixer': Mixer,
    }
    talent = models.IntegerField(choices=Talent_Choices, null=True, blank=True)

    def __iter__(self):
        return iter(self.Talent_Choices)

    def __str__(self):
        return self.Talent_Choices[self.talent][1]

class Entertaener(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=32, default='anonymous');

    latitude = models.FloatField(default=33.7490)
    longitude = models.FloatField(default=-84.3880)

    talent = models.ManyToManyField(Talent)
    equipment = models.CharField(max_length=200, blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    pitch = models.CharField(max_length=5000, blank=True, null=True)

    contacts = models.ManyToManyField('self', symmetrical=False, related_name='contacted')

    portfolio = models.URLField(blank=True, null=True)
    picture = models.ImageField(upload_to=imgUploadLocation, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Entertaener.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

class PortfolioLink(models.Model):
    entertaener = models.ForeignKey(Entertaener, on_delete=models.CASCADE, related_name='portfolioLink')
    link = models.URLField()
