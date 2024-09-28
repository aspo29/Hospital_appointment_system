from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from appointments.models import Appointment  # Adjust import as necessary
from appointments.views import update_appointment, delete_appointment
from django.contrib import messages
from patients.models import Patient 

@login_required
def profile(request):
    if request.method == 'POST':
        print("Form is submitted")  # Debugging line
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            print("User Form Errors:", user_form.errors)  # Debugging line
            print("Profile Form Errors:", profile_form.errors)  # Debugging line
            messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        user_form = UserUpdateForm(instance=request.user)

    # Only fetch appointments if the user is not staff/admin
    appointments = Appointment.objects.filter(patient__user=request.user) if not request.user.is_staff else None
    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'appointments': appointments,
    }
    return render(request, 'profiles/profile.html', context)

@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile = request.user.profile  # Get the user's profile

        # Update the profile picture
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()

        messages.success(request, 'Profile picture updated successfully.')
        return redirect('profile')  # Redirect to the profile page
    messages.error(request, 'Failed to upload picture.')
    return redirect('profile')

@login_required
def delete_account(request):
    if request.method == 'POST':
        # Delete all appointments related to the user
        Appointment.objects.filter(patient__user=request.user).delete()

        # Delete the patient profile associated with the user, if exists
        patient = Patient.objects.filter(user=request.user).first()
        if patient:
            patient.delete()  # Delete the patient profile

        # Delete the user account
        request.user.delete()
        
        messages.success(request, "Your account and associated data have been deleted successfully.")
        return redirect('home')  # Redirect to the home page or a specific page after deletion