from django import forms
from django.contrib.auth.models import User
from .enums import JobRole
from .models import Client, Staff, Job, Qualification

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'company_name',
            'address_line_1',
            'address_line_2',
            'town',
            'county',
            'postcode',
            'phone_number',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'required': True}),
        }

class UserForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Select a Client", required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
    username = forms.CharField(required=True, label="Username")



    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'client', 'password']


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name']



class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['role']
        widgets = {
            'role': forms.Select(choices=[(role.name, role.value) for role in JobRole])
        }


class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['job', 'name', 'passed_date', 'expiry_date']
        widgets = {
            'passed_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
