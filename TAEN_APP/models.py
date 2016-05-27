from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Talent(models.Model):
    Recording = 'R'
    Musician = 'M'
    Producer = 'P'
    Talent_Choices = (
            (Recording, 'Recording'),
            (Musician, 'Musician'),
            (Producer, 'Producer'),
    )
    talent = models.CharField(max_length=1, choices=Talent_Choices, blank=True)

    def __str__(self):
        return talent

class Entertaener(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    name = models.CharField(max_length = 32, default='anonymous');

    talent = models.ForeignKey(Talent, null=True)

    pitch = models.CharField(max_length=5000, blank=True, null=True)

    portfolio = models.URLField(blank=True, null=True)
    picture = models.ImageField(upload_to='profile_images', blank=True, null=True)

    def __str__(self):
        return self.user.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Entertaener.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)
