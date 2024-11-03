from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from cms.models import Speciality
# Create your models here.

class Appointment(models.Model):
    TIME_LIST = (
        (0, '09:00 – 10:00'),
        (1, '10:00 – 11:00'),
        (2, '11:00 – 12:00'),
        (3, '12:00 – 13:00'),
        (4, '13:00 – 14:00'),
        (5, '14:00 – 15:00'),
        (6, '15:00 – 16:00'),
        (7, '16:00 – 17:00'),
        (8, '17:00 – 18:00'),
    )
    PRICE_CATEGORY_CHOICES = [
        (1, "Standard - NPR 500"),
        (2, "Premium - NPR 1000"),
        (3, "VIP - NPR 1500"),
    ]
    id = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True,related_name='appointments')
    specialty = models.ForeignKey(Speciality, on_delete=models.CASCADE, null=True)
    symptom_description = models.TextField(default='', blank=True)
    appointment_date = models.DateField(null=True)
    appointment_time = models.IntegerField(choices=TIME_LIST, null=True)
    price_category = models.IntegerField(choices=PRICE_CATEGORY_CHOICES, default=1)

    def __str__(self):
        return f'Appointment with Dr. {self.doctor.name} for {self.patient.name} on {self.appointment_date} at {self.time}'
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Calculate the next ID
            last_appointment = Appointment.objects.order_by('-id').first()
            if last_appointment:
                self.id = last_appointment.id + 1
            else:
                self.id = 1
        super().save(*args, **kwargs)

    @property
    def time(self):
        if self.appointment_time is not None:
            return self.TIME_LIST[self.appointment_time][1]
        return None
    
    def get_price_in_npr(self):
        price_mapping = {1: 500, 2: 1000, 3: 1500}
        return price_mapping.get(self.price_category, 500)