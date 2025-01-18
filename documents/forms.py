from django import forms
from .models import Document



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

