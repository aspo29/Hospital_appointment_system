from django import forms
from .models import Speciality 

class LoginForm(forms.Form):
     username = forms.CharField(max_length=150, label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}))
     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}), label='Password')

class RegistrationForm(forms.Form):
    username = forms.CharField( max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),label='Username')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),label='Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')

class SpecialityForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = ['name', 'description', 'original_price', 'discounted_price', 'discount', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
            'original_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter original price'}),
            'discounted_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter discounted price'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter discount'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

