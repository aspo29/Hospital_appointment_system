from django.db import models
from appointments.models import Appointment
class Payment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="payment",null=True)
    patient_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=20, blank=True, default='EPAYTEST')  # fixed default value
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for {self.patient_name} - NPR {self.price}"