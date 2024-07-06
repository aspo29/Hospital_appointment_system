from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404 , HttpResponse, HttpResponseRedirect ,JsonResponse
from django.template.loader import render_to_string
from patients.forms import PatientForm 
from .forms import AppointmentForm
from .models import Speciality ,Appointment 
from appointments.models import Appointment
from doctors.models import Doctor
from patients.models import Patient
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
import os
# Create your views here.

def book_appointment(request):
    if not request.user.is_authenticated and request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        patient_form = PatientForm(request.POST)
        appointment_form = AppointmentForm(request.POST, show_patient_field=False)
        
        if patient_form.is_valid() and appointment_form.is_valid():
            patient = patient_form.save()
            
            doctor = appointment_form.cleaned_data['doctor']
            specialty = appointment_form.cleaned_data['specialty']
            appointment_date = appointment_form.cleaned_data['appointment_date']
            appointment_time = appointment_form.cleaned_data['appointment_time']
            symptom_description = appointment_form.cleaned_data['symptom_description']
            
            appointment = Appointment(
                patient=patient,
                doctor=doctor,
                specialty=specialty,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                symptom_description=symptom_description
            )
            appointment.save()
        
            messages.success(request, 'You will soon receive a contact from the hospital.')

            request.session['appointment_id'] = appointment.id
            
            return redirect('success_view', appointment_id=appointment.id)
    
    else:
        doctor_id = request.GET.get('doctor_id')
        speciality_id = request.GET.get('speciality_id')
        initial_data = {}
        if doctor_id:
            initial_data['doctor'] = Doctor.objects.get(pk=doctor_id)
        if speciality_id:
            initial_data['specialty'] = Speciality.objects.get(pk=speciality_id)

        patient_form = PatientForm()
        appointment_form = AppointmentForm(initial=initial_data, show_patient_field=False)
    
    context = {
        'patient_form': patient_form,
        'appointment_form': appointment_form,
        'doctors': Doctor.objects.all(),
        'specialities': Speciality.objects.all(),
    }
    return render(request, 'appointments/book_appointment.html', context)

def book_another_appointment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        try:
            patient = Patient.objects.get(name=patient_name)
        except Patient.DoesNotExist:
            messages.error(request, 'Patient not found. Please create a new appointment.')
            return redirect('book_appointment')

        appointment_form = AppointmentForm(request.POST, show_patient_field=False)
        if appointment_form.is_valid():
            doctor = appointment_form.cleaned_data['doctor']
            specialty = appointment_form.cleaned_data['specialty']
            appointment_date = appointment_form.cleaned_data['appointment_date']
            appointment_time = appointment_form.cleaned_data['appointment_time']
            symptom_description = appointment_form.cleaned_data['symptom_description']

            appointment = Appointment(
                patient=patient,
                doctor=doctor,
                specialty=specialty,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                symptom_description=symptom_description
            )
            appointment.save()

            messages.success(request, 'You will soon receive a contact from the hospital.')

            request.session['appointment_id'] = appointment.id

            return redirect('success_view', appointment_id=appointment.id)
    else:
        appointment_form = AppointmentForm(show_patient_field=False)

    context = {
        'appointment_form': appointment_form,
    }
    return render(request, 'appointments/book_another_appointment.html', context)


# List appointments
def appointment_list(request):
    if not request.user.is_staff:
        return redirect('login')
    appointments = Appointment.objects.all().order_by('id')
    context = {'appointments': appointments}
    return render(request, 'appointments/appointment_list.html', context)


DEFAULT_PATIENT_ID = 1
# Add appointment
def add_appointment(request):
    if not request.user.is_staff:
        return redirect('login')

    default_patient = Patient.objects.get(pk=DEFAULT_PATIENT_ID)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor = form.cleaned_data['doctor']
            specialty = form.cleaned_data['specialty']
            appointment_date = form.cleaned_data['appointment_date']
            appointment_time = form.cleaned_data['appointment_time']
            symptom_description = form.cleaned_data['symptom_description']
            
            appointment = Appointment(
                patient=default_patient,  
                doctor=doctor,
                specialty=specialty,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                symptom_description=symptom_description
            )
            appointment.save()
            messages.success(request, 'Appointment added successfully.')
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    
    return render(request, 'appointments/add_appointment.html', {'form': form})

# Delete appointment
def delete_appointment(request, appointment_id):
    if not request.user.is_staff:
        return redirect('login')
    
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully.')
        return redirect('appointment_list')

    return render(request, 'appointments/appointment_list.html', {'appointment': appointment})

def update_appointment(request, appointment_id):
    if not request.user.is_staff:
        return redirect('login')
    default_patient = Patient.objects.get(pk=DEFAULT_PATIENT_ID)

    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated successfully.')
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointments/update_appointment.html', {'form': form, 'appointment': appointment})

@login_required
def success_view(request, appointment_id):
    if not appointment_id:
        raise Http404("Appointment ID not provided")
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if not request.user.is_authenticated and request.user.is_staff:
        return redirect('login')
    # appointment = Appointment.objects.all().order_by('-id').first()
    if appointment:
        context = {'appointment': appointment}
    else:
        context = {} 
    return render(request, 'appointments/success.html', context)

def ticket(request):
    if 'appointment_id' not in request.session:
        return HttpResponse('Appointment ID not found in session.')

    appointment_id = request.session['appointment_id']
    appointment = Appointment.objects.get(pk=appointment_id)

    # Generate token
    year_last_two = str(appointment.appointment_date.year)[-2:]  
    date_two_digits = appointment.appointment_date.strftime('%d')  
    id_two_digits = '{:02d}'.format(appointment.id % 100) 
    template_path = 'appointments/ticket.html'  

    token = f"{year_last_two}{date_two_digits}{id_two_digits}"

    template = get_template(template_path)
    context = {
        'appointment': appointment,
        'token': token,
    }
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="ticket.pdf"'

    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=lambda uri, _: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    )

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response

def get_specialty_by_doctor(request):
    doctor_id = request.GET.get('doctor_id')
    selected_specialty = None
    if doctor_id:
        doctor = Doctor.objects.get(id=doctor_id)
        specialties = Speciality.objects.filter(profession__doctor=doctor)
        if specialties.exists():
            selected_specialty = specialties.first().id  
    else:
        specialties = Speciality.objects.none()
    html = render_to_string('appointments/specialty_options.html', {'specialties': specialties})
    return JsonResponse({'html': html, 'selected_specialty': selected_specialty})

def get_doctor_by_specialty(request):
    specialty_id = request.GET.get('specialty_id')
    selected_doctor = None
    if specialty_id:
        specialty = Speciality.objects.get(id=specialty_id)
        doctors = Doctor.objects.filter(profession__speciality=specialty)
        if doctors.exists():
            selected_doctor = doctors.first().id  
    else:
        doctors = Doctor.objects.none()
    html = render_to_string('appointments/doctor_options.html', {'doctors': doctors})
    return JsonResponse({'html': html, 'selected_doctor': selected_doctor})