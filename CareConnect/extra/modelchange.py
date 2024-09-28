# from patients.models import Patient

# patients = Patient.objects.all().order_by('id')
# list(map(lambda patient, new_id: Patient.objects.filter(pk=patient.pk).update(id=new_id), patients, range(1, len(patients) + 1)))