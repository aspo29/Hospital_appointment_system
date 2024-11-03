from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from payments.models import Payment

@receiver(post_save, sender=Appointment)
def create_payment_for_appointment(sender, instance, created, **kwargs):
    if created:
        # Create a Payment record linked to the new Appointment
        Payment.objects.create(
            appointment=instance,  # Link the payment to the appointment
            patient_name=instance.patient.name,  # Assuming `patient` has a `name` field
            price=instance.get_price_in_npr()
        )