from django.db import models
from django.contrib.auth.models import User
from appointments.models import Appointment

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(default='default.jpg',upload_to='profile_pics/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True) 

    def __str__(self):
        return f'{self.user.username} Profile'