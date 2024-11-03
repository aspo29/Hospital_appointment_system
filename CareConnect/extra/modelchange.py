# from patients.models import Patient

# patients = Patient.objects.all().order_by('id')
# list(map(lambda patient, new_id: Patient.objects.filter(pk=patient.pk).update(id=new_id), patients, range(1, len(patients) + 1)))

# from django.contrib.auth.models import User
# from profile.models import Profile  # Replace `yourapp` with the app name where Profile is defined

# for user in User.objects.all():
#     Profile.objects.get_or_create(user=user)