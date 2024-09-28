from django.shortcuts import render, redirect ,get_object_or_404
from .forms import DoctorForm 
from .models import Doctor 
from cms.models import Speciality
from django.contrib import messages

def find_doctors(request, speciality_id=None):
    if speciality_id:
        speciality = get_object_or_404(Speciality, id=speciality_id)
        doctors = Doctor.objects.filter(profession__speciality=speciality)
    else:
        doctors = Doctor.objects.all()

    is_authenticated = request.user.is_authenticated
    is_staff = request.user.is_staff
    has_appointment = request.session.get('appointment_id') is not None  # Check for existing appointment

    return render(request, 'doctors/find_doctors.html', {
        'doctors': doctors,
        'selected_speciality_id': speciality_id,
        'is_authenticated': is_authenticated,
        'is_staff': is_staff,
        'has_appointment': has_appointment,  # Pass this variable to the template
    })

# Doctor views
def doctor_list(request):
    if not request.user.is_staff:
        return redirect('login')
    docs = Doctor.objects.all().order_by('id')
    context = {'docs': docs}
    return render(request, 'doctors/doctor_list.html', context)

def delete_doctor(request, doctor_id):
    if not request.user.is_staff:
        return redirect('login')
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    if request.method == 'POST':
        doctor.delete()
        remaining_doctors = Doctor.objects.all()
        for index, doctor in enumerate(remaining_doctors, start=1):
            doctor.id = index
            doctor.save()
        messages.success(request, 'Doctor deleted successfully.')
        return redirect('doctor_list')
    return redirect('doctor_list')


def add_doctor(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor added successfully.')
            # time.sleep(2)
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'doctors/add_doctor.html', {'form': form})

def update_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor details updated successfully.')
            return redirect('doctor_list')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'doctors/update_doctor.html', {'form': form, 'doctor': doctor})