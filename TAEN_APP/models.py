from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os

def imgUploadLocation(instance, filename):
    return "%s/%s/%s" %(instance, 'profile', filename)

def ProjectImgUploadLocation(instance, filename):
    return "%s/%s/%s/%s" %(instance.entertaener, 'project', instance, filename)

def ToolImgUploadLocation(instance, filename):
    return "%s/%s/%s/%s" %(instance.entertaener, 'tool', instance, filename)

class Talent(models.Model):
    Artist = 0
    Producer = 1
    RecordingEngineer = 2
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
    gender = models.CharField(max_length=12, null=True, blank=True)
    picture = models.ImageField(upload_to=imgUploadLocation, blank=True, null=True)

    latitude = models.FloatField(default=33.7490)
    longitude = models.FloatField(default=-84.3880)
    city = models.CharField(max_length=50, default='Atlanta')
    state = models.CharField(max_length=50, default='GA')

    talent = models.ManyToManyField(Talent, related_name='entertaeners')
    genres = models.CharField(max_length=200, default='All')
    pitch = models.CharField(max_length=5000, blank=True, null=True)

    contacts = models.ManyToManyField('self', symmetrical=False, related_name='contacted')

    def __str__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Entertaener.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

class PortfolioLink(models.Model):
    entertaener = models.ForeignKey(Entertaener, on_delete=models.CASCADE, related_name='portfolioLink')
    link = models.URLField()
    title = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        if title is None:
            return self.link
        return self.title

class Project(models.Model):
    entertaener = models.ForeignKey(Entertaener, on_delete=models.CASCADE, related_name='project')
    title = models.CharField(max_length=32, null=True, blank=True)
    contributors = models.CharField(max_length=259, null=True, blank=True)
    description = models.CharField(max_length=2500, null=True, blank=True)
    link = models.URLField()
    image = models.ImageField(upload_to=ProjectImgUploadLocation, blank=True, null=True)

    def __str__(self):
        return self.title

class Tool(models.Model):
    entertaener = models.ForeignKey(Entertaener, on_delete=models.CASCADE, related_name='tool')
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to=ToolImgUploadLocation, blank=True, null=True)

    def __str__(self):
        return self.title
