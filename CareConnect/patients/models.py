from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    mobile = models.CharField(max_length=15)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Calculate the next ID
            last_patient = Patient.objects.order_by('-id').first()
            if last_patient:
                self.id = last_patient.id + 1
            else:
                self.id = 1
        super().save(*args, **kwargs)
