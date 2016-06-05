from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os

def imgUploadLocation(instance, filename):
    return "%s/%s" %(instance.id, filename)

class Talent(models.Model):
    Recording = 0
    Musician = 1
    Producer = 2
    Talent_Choices = [
            (Recording, 'Recording'),
            (Musician, 'Musician'),
            (Producer, 'Producer'),
    ]
    Talent_Dictionary = {
            'Recording': Recording,
            'Musician': Musician,
            'Producer': Producer,
    }
    talent = models.IntegerField(choices=Talent_Choices, null=True, blank=True)

    def __iter__(self):
        return iter(self.Talent_Choices)

    def __str__(self):
        return self.Talent_Choices[self.talent][1]

class Entertaener(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length = 32, default='anonymous');

    talent = models.ManyToManyField(Talent)
    contacts = models.ManyToManyField('self')

    pitch = models.CharField(max_length=5000, blank=True, null=True)

    portfolio = models.URLField(blank=True, null=True)
    picture = models.ImageField(upload_to=imgUploadLocation, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Entertaener.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)
