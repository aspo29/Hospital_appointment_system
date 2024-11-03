from django.shortcuts import render, redirect ,get_object_or_404
from django.urls import reverse
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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient, Appointment, Doctor, Speciality


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Patient, Appointment, Doctor, Speciality
from .forms import  AppointmentForm
from patients.forms import PatientForm

@login_required
def book_appointment(request):
    # Attempt to fetch the existing Patient instance for the logged-in user
    patient = Patient.objects.filter(user=request.user).first()

    if request.method == 'POST':
        # Get the forms with the POST data
        patient_form = PatientForm(request.POST, instance=patient)  # Link the form to the existing patient if it exists
        appointment_form = AppointmentForm(request.POST, show_patient_field=False)

        # First, validate the appointment form
        if appointment_form.is_valid():
            # Now create or update the patient profile if necessary
            if not patient:
                # If no patient exists, create a new Patient instance
                if patient_form.is_valid():
                    patient = patient_form.save(commit=False)
                    patient.user = request.user  # Link patient to the logged-in user
                    patient.save()  # Save the new patient
                    messages.success(request, "Patient profile created successfully.")
                else:
                    messages.error(request, "Invalid patient information.")
                    return render(request, 'appointments/book_appointment.html', {
                        'patient_form': patient_form,
                        'appointment_form': appointment_form,
                    })

            # Now associate the appointment with the patient
            appointment = appointment_form.save(commit=False)
            appointment.patient = patient  # Associate the appointment with the patient
            appointment.save()  # Save the appointment

            # messages.success(request, 'Appointment created successfully. You will soon be contacted by the hospital.')
            # request.session.pop('appointment_form_data', None)
            # request.session.pop('patient_form_data', None)
            # return redirect('success_view', appointment_id=appointment.id)
            # Display success message
            # Store appointment ID in session
            messages.success(request, 'Appointment created successfully. You will be redirected to checkout.')
            # Redirect to checkout page in the payment app with patient ID and price
            return redirect(reverse('payment:checkout', args=[appointment.patient.id, appointment.get_price_in_npr()]))
        else:
            # Save form data to session if not valid
            request.session['appointment_form_data'] = request.POST
            request.session['patient_form_data'] = request.POST
    else:
        # Pre-populate forms with session data if available
        appointment_form_data = request.session.get('appointment_form_data')
        patient_form_data = request.session.get('patient_form_data')
        
        if appointment_form_data:
            appointment_form = AppointmentForm(appointment_form_data, show_patient_field=False)
        else:
            initial_data = {}
            if doctor_id := request.GET.get('doctor_id'):
                initial_data['doctor'] = Doctor.objects.get(pk=doctor_id)
            if speciality_id := request.GET.get('speciality_id'):
                initial_data['specialty'] = Speciality.objects.get(pk=speciality_id)
            appointment_form = AppointmentForm(initial=initial_data, show_patient_field=False)

        if patient_form_data:
            patient_form = PatientForm(patient_form_data)
        else:
            patient_form = PatientForm(instance=patient)

    context = {
        'patient_form': patient_form,
        'appointment_form': appointment_form,
        'doctors': Doctor.objects.all(),
        'specialities': Speciality.objects.all(),
    }
    return render(request, 'appointments/book_appointment.html', context)

@login_required
def book_another_appointment(request):
    # Retrieve the patient's record based on the logged-in user
    patient = Patient.objects.filter(user=request.user).first()
    if not patient:
        messages.error(request, 'No patient found. Please book your first appointment.')
        return redirect('appointment:book_appointment')

    # Get doctor and specialty from query parameters if available
    doctor_id = request.GET.get('doctor_id')
    speciality_id = request.GET.get('speciality_id')
    doctor = Doctor.objects.filter(id=doctor_id).first() if doctor_id else None
    specialty = Speciality.objects.filter(id=speciality_id).first() if speciality_id else None

    # Check if this is a POST request to process form data
    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST, show_patient_field=False)
        
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            appointment.patient = patient

            # Set doctor and specialty if provided in the query parameters
            if doctor:
                appointment.doctor = doctor
            if specialty:
                appointment.specialty = specialty

            # Check for time conflicts with other appointments for the same patient
            existing_appointments = Appointment.objects.filter(
                patient=patient,
                appointment_date=appointment.appointment_date,
                appointment_time=appointment.appointment_time
            )
            if existing_appointments.exists():
                messages.error(request, 'You already have an appointment at this time.')
            else:
                # Save the appointment and proceed to checkout
                appointment.save()
                messages.success(request, 'Appointment created successfully. You will be redirected to checkout.')
                
                # Redirect to checkout with patient ID and price
                return redirect(reverse('payment:checkout', args=[appointment.patient.id, appointment.get_price_in_npr()]))
        else:
            # Save form data in session if there are errors, so it can be restored
            request.session['appointment_form_data'] = request.POST

    else:
        # Load form data from session or initialize with doctor and specialty data
        initial_data = {}
        if doctor:
            initial_data['doctor'] = doctor
        if specialty:
            initial_data['specialty'] = specialty

        appointment_form_data = request.session.get('appointment_form_data')
        appointment_form = AppointmentForm(appointment_form_data or None, show_patient_field=False, initial=initial_data)

    # Prepare the context for rendering the template
    context = {
        'appointment_form': appointment_form,
        'patient_name': patient.name,
    }
    return render(request, 'appointments/book_another_appointment.html', context)

# List appointments
def appointment_list(request):
    if not request.user.is_staff:
        return redirect('login')
    appointments = Appointment.objects.all().order_by('id')
    context = {'appointments': appointments}
    return render(request, 'appointments/appointment_list.html', context)

DEFAULT_PATIENT_ID = 1  # Make sure to set this appropriately in your settings or context

@login_required
def add_appointment(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('profile')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor = form.cleaned_data['doctor']
            specialty = form.cleaned_data['specialty']
            appointment_date = form.cleaned_data['appointment_date']
            appointment_time = form.cleaned_data['appointment_time']
            symptom_description = form.cleaned_data['symptom_description']

            # Get the patient ID from the form data (make sure to include this in your form)
            patient_id = request.POST.get('patient_id')
            patient = get_object_or_404(Patient, id=patient_id)

            # Create the appointment
            appointment = Appointment(
                patient=patient,
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

    # Get all patients for the admin to select from
    patients = Patient.objects.all()
    return render(request, 'appointments/add_appointment.html', {'form': form, 'patients': patients})

# # Delete appointment
# def delete_appointment(request, appointment_id):
#     if not request.user.is_staff:
#         return redirect('login')
    
#     appointment = get_object_or_404(Appointment, pk=appointment_id)
    
#     if request.method == 'POST':
#         appointment.delete()
#         messages.success(request, 'Appointment deleted successfully.')
#         return redirect('appointment_list')

#     return render(request, 'appointments/appointment_list.html', {'appointment': appointment})

# def update_appointment(request, appointment_id):
#     if not request.user.is_staff:
#         return redirect('login')
#     default_patient = Patient.objects.get(pk=DEFAULT_PATIENT_ID)

#     appointment = get_object_or_404(Appointment, id=appointment_id)
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST, instance=appointment)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Appointment updated successfully.')
#             return redirect('appointment_list')
#     else:
#         form = AppointmentForm(instance=appointment)
#     return render(request, 'appointments/update_appointment.html', {'form': form, 'appointment': appointment})
@login_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # If the user is not an admin, check if they are the patient associated with the appointment
    if not request.user.is_staff and appointment.patient.user != request.user:
        messages.error(request, 'You do not have permission to edit this appointment.')
        return redirect('profile')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            if request.user.is_staff:
                messages.success(request, 'Appointment updated successfully.')
                return redirect('appointment_list')
            else:
                messages.success(request, 'Your appointment has been updated successfully.')
                return redirect('profile')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointments/update_appointment.html', {'form': form, 'appointment': appointment})

@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    # Check permissions
    if not request.user.is_staff and appointment.patient.user != request.user:
        messages.error(request, 'You do not have permission to delete this appointment.')
        return redirect('profile')

    # Handle the deletion if the request is a POST
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully.')
        # Redirect based on user type
        return redirect('appointment_list' if request.user.is_staff else 'profile')

    # Render confirmation template for GET request
    return render(request, 'appointments/confirm_delete.html', {'appointment': appointment})

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

def ticket(request, appointment_id):
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        return HttpResponse('Appointment not found.')

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