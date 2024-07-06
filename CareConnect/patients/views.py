from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib import messages
from .forms import  PatientForm
from .models import Patient 

# Create your views here.
# Patient views
def patient_list(request):
    if not request.user.is_staff:
        return redirect('login')
    patients = Patient.objects.all().order_by('id')
    context = {'patients': patients}
    return render(request, 'patients/patient_list.html', context)

def delete_patient(request, patient_id):
    if not request.user.is_staff:
        return redirect('login')
    
    patient = get_object_or_404(Patient, pk=patient_id)
    
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully.')
    return redirect('patient_list')

def add_patient(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient added successfully.')
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/add_patient.html', {'form': form})

def update_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient details updated successfully.')
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/update_patient.html', {'form': form, 'patient': patient})