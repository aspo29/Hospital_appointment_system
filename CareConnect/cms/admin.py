from django.contrib import admin
from .models import  Speciality ,Profession

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'original_price', 'discounted_price', 'discount','image')

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'speciality')
    search_fields = ('name',)
    list_filter = ('speciality',)

# Alternatively, you can use admin.site.register if you don't want to use the decorator style

# admin.site.register(Doctor, DoctorAdmin)
# admin.site.register(Patient, PatientAdmin)
# admin.site.register(Appointment, AppointmentAdmin)
