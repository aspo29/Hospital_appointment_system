from django.db import models
from cms.models import Profession 
# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='doctor_images/', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            latest_doctor = Doctor.objects.order_by('-id').first()
            if latest_doctor:
                self.id = latest_doctor.id + 1
            else:
                self.id = 1
        return super().save(*args, **kwargs)