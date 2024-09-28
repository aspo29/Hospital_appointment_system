from django import forms
from .models import Speciality ,Appointment
from doctors.models import Doctor
from patients.models import Patient
from datetime import date
# from .widgets import ImageRadioSelect


PAYMENT_CHOICES = [
    ('fonepay', 'FonePay'),
    ('khalti', 'Khalti'),
    ('hbl', 'HBL'),
    ('esewa', 'eSewa'),
]

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), empty_label="Select Doctor", required=True, label='Doctor', widget=forms.Select(attrs={'class': 'form-select'}))
    specialty = forms.ModelChoiceField(queryset=Speciality.objects.all(), empty_label="Select Specialty", required=True, label='Specialty', widget=forms.Select(attrs={'class': 'form-select'}))
    appointment_date = forms.DateField(initial=date.today, widget=forms.SelectDateWidget(years=range(date.today().year, date.today().year + 1), attrs={'class': 'form-select mx-2', 'style': 'width: 30.5%; display: inline-block;'}), required=True, label='Date')
    appointment_time = forms.ChoiceField(required=True, label='Time', widget=forms.Select(attrs={'class': 'form-select'}))
    symptom_description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=False, label='Symptoms (if any)')
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, label='Select Payment Method', widget=forms.RadioSelect(attrs={'class': 'radio-choice','style':'display: inline-block; margin-right: 10px;'}))

    class Meta:
        model = Appointment
        fields = ['doctor', 'specialty', 'appointment_date', 'appointment_time', 'symptom_description', 'payment_method']

    def __init__(self, *args, **kwargs):
        show_patient_field = kwargs.pop('show_patient_field', True)
        super().__init__(*args, **kwargs)

        # Set choices for appointment_time based on TIME_LIST in the Appointment model
        self.fields['appointment_time'].choices = Appointment.TIME_LIST