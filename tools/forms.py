from django import forms
from .models import ToolEquipment, CalibrationTest

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