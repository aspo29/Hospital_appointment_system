from django.contrib import admin

# Register your models here.
from .models import Patient 


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'mobile', 'address')
    search_fields = ('name', 'mobile')
    list_filter = ('gender',)