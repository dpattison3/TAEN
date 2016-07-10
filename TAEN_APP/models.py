from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os

def imgUploadLocation(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Talent(models.Model):
    RecordingEngineer = 0
    Artist = 1
    Producer = 2
    SoundMixer = 3
    Talent_Choices = [
            (Artist, 'Artist'),
            (Producer, 'Producer'),
            (RecordingEngineer, 'Recording Engineer'),
            (SoundMixer, 'Sound Mixer'),
    ]
    Talent_Dictionary = {
            'Artist': Artist,
            'Producer': Producer,
            'Recording Engineer': RecordingEngineer,
            'Sound Mixer': SoundMixer,
    }
    talent = models.IntegerField(choices=Talent_Choices)

    def __iter__(self):
        return iter(self.Talent_Choices)

    def __str__(self):
        return self.Talent_Choices[self.talent][1]

class Entertaener(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=32, default='anonymous');
    age = models.PositiveSmallIntegerField(null=True, blank=True)

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

    def __str__(self):
        return self.link
