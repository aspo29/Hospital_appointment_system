from django.contrib import admin
from .models import  Speciality ,Profession ,MedicalService, CarouselImage ,StaticFile

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'original_price', 'discounted_price', 'discount','image')

@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'speciality')
    search_fields = ('name',)
    list_filter = ('speciality',)


@admin.register(MedicalService)
class MedicalServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'original_price', 'discounted_price', 'discount', 'badge', 'url')
    search_fields = ('name', 'description')
    list_filter = ('discount', 'badge')

@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'interval')
    search_fields = ('id',)

@admin.register(StaticFile)
class StaticFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image')
    search_fields = ('id', 'name')

# Alternatively, you can use admin.site.register if you don't want to use the decorator style

# admin.site.register(Doctor, DoctorAdmin)
# admin.site.register(Patient, PatientAdmin)
# admin.site.register(Appointment, AppointmentAdmin)
