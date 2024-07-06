from django import forms
from .models import Patient
class PatientForm(forms.ModelForm):
    gender_choices = [('', 'Select Gender'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other')]

    gender = forms.ChoiceField(choices=gender_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Patient
        fields = ['name', 'age', 'gender', 'mobile', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter age'}),
            # 'gender': forms.Select(attrs={'class': 'form-control'},choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')]),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
        }
