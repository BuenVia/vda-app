from django import forms
from django.contrib.auth.models import User
from .enums import JobRole
from .models import Client, Staff, Job, Qualification, ToolEquipment, CalibrationTest, Document

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



class ToolEquipmentForm(forms.ModelForm):
    class Meta:
        model = ToolEquipment
        fields = ['make', 'model', 'description']


class CalibrationTestForm(forms.ModelForm):
    class Meta:
        model = CalibrationTest
        fields = ['test_name', 'test_completion_date', 'test_renewal_date', 'test_score']
        widgets = {
            'test_completion_date': forms.DateInput(attrs={'type': 'date'}),
            'test_renewal_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")
            if file.size > 10 * 1024 * 1024:  # 10MB limit
                raise forms.ValidationError("File size must be under 10MB.")
        return file


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        required=False,
        label='Password'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # Update password only if provided
        if commit:
            user.save()
        return user
