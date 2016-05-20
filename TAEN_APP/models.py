from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Entertaener(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length = 32, default='anonymous');
    email = models.EmailField();

    portfolio = models.URLField(blank=true)
    picture = models.ImageField(upload_to='profile_images', blank=true)

    def __str__(self):
        return self.user.username
