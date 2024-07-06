from django.shortcuts import render, redirect ,get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login as auth_login ,logout
from django.contrib import messages
from .forms import LoginForm ,RegistrationForm ,SpecialityForm 
from django.contrib.auth.models import User
import time
from .models import Speciality 
from appointments.models import Appointment
from doctors.models import Doctor
from patients.models import Patient
from django.db.models import Count
from urllib.parse import urlparse, parse_qs, unquote

class HomeView(TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Aggregate counts
        doctor_count = Doctor.objects.aggregate(d=Count('id'))
        patient_count = Patient.objects.aggregate(p=Count('id'))
        speciality_count = Speciality.objects.aggregate(s=Count('id'))
        appointment_count = Appointment.objects.aggregate(a=Count('id'))

        # Update context with aggregated counts
        context.update({
            'doctor_count': doctor_count['d'],
            'patient_count': patient_count['p'],
            'speciality_count': speciality_count['s'],
            'appointment_count': appointment_count['a'],
        })

        return context

def index(request):
    specialities = Speciality.objects.all()
    return render(request, 'index.html', {'specialities': specialities})

def contact_us(request):
    return render(request, 'cms/contact_us.html')

def about_us(request):
    return render(request, 'cms/about_us.html')

def login(request):
    next_url = request.GET.get('next', '')  # Get the next parameter from the URL
    next_url = unquote(next_url)  # Decode the next parameter if it's encoded

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                if next_url:
                    return redirect(next_url)  # Redirect to the next URL if it exists
                elif user.is_staff:
                    return redirect('home')  # Redirect to home page for staff users
                else:
                    return redirect('index')  # Redirect to a different page for non-staff users
            else:
                return render(request, 'cms/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'cms/login.html', {'form': form, 'next': next_url})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'Registration successful! Please log in.')
                    return redirect('login')
            else:
                messages.error(request, 'Passwords do not match')
    else:
        form = RegistrationForm()
    return render(request, 'cms/register.html', {'form': form})

def logout_admin(request):
    if request.user.is_authenticated and request.user.is_staff:
        logout(request)
        messages.success(request, 'Admin has successfully logged out.')
    return redirect('login')

def logout_user(request):
    if request.user.is_authenticated and not request.user.is_staff:
        logout(request)
        messages.success(request, 'You have successfully logged out.')
    return redirect('login')


def home (request):
    if not request.user.is_staff:
        return redirect(login)
    return render (request,'home.html')


def specialty_list(request):
    specialties = Speciality.objects.all()
    return render(request, 'cms/speciality_list.html', {'specialties': specialties})

def add_specialty(request):
    if request.method == 'POST':
        form = SpecialityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('specialty_list')
    else:
        form = SpecialityForm()
    return render(request, 'cms/add_speciality.html', {'form': form})


def delete_specialty(request, specialty_id):
    if not request.user.is_staff:
        return redirect('login')
    
    specialty = get_object_or_404(Speciality, pk=specialty_id)
    
    if request.method == 'POST':
        specialty.delete()
        messages.success(request, 'Specialty deleted successfully.')
    return redirect('specialty_list')

def update_specialty(request, specialty_id):
    specialty = get_object_or_404(Speciality, id=specialty_id)
    if request.method == 'POST':
        form = SpecialityForm(request.POST, request.FILES, instance=specialty)
        if form.is_valid():
            form.save()
            messages.success(request, 'Specialty updated successfully.')
            return redirect('specialty_list')
    else:
        form = SpecialityForm(instance=specialty)
    return render(request, 'cms/update_specialty.html', {'form': form, 'specialty': specialty})