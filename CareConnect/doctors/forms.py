from django import forms
from .models import Doctor
from cms.models import Profession
class DoctorForm(forms.ModelForm):
    profession = forms.ModelChoiceField(queryset=Profession.objects.all(), empty_label="Select Profession", widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'mobile', 'profession', 'image'] 
        widgets = {
            'id': forms.HiddenInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}) 
        }