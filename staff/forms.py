from django import forms
from .models import Staff, StaffJob, StaffQualification, JobTypes

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name']



class JobForm(forms.ModelForm):
    job = forms.ModelChoiceField(
        queryset=JobTypes.objects.all(),
        empty_label="Select Job Type",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = StaffJob
        fields = ['job']


class QualificationForm(forms.ModelForm):
    class Meta:
        model = StaffQualification
        fields = ['job', 'name', 'passed_date', 'expiry_date']
        widgets = {
            'passed_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }