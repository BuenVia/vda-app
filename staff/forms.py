from django import forms
from .enums import JobRole
from .models import Staff, StaffJob, StaffQualification

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name']



class JobForm(forms.ModelForm):
    class Meta:
        model = StaffJob
        fields = ['role']
        widgets = {
            'role': forms.Select(choices=[(role.name, role.value) for role in JobRole])
        }


class QualificationForm(forms.ModelForm):
    class Meta:
        model = StaffQualification
        fields = ['job', 'name', 'passed_date', 'expiry_date']
        widgets = {
            'passed_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }