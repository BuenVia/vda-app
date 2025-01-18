# from django import forms
# from django.contrib.auth.models import User
# from .models import Client

# class ClientForm(forms.ModelForm):
#     class Meta:
#         model = Client
#         fields = [
#             'company_name',
#             'address_line_1',
#             'address_line_2',
#             'town',
#             'county',
#             'postcode',
#             'phone_number',
#         ]
#         widgets = {
#             'company_name': forms.TextInput(attrs={'required': True}),
#         }

# class UserForm(forms.ModelForm):
#     client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label="Select a Client", required=True)
#     password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")
#     username = forms.CharField(required=True, label="Username")



#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'client', 'password']


# class UserUpdateForm(forms.ModelForm):
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
#         required=False,
#         label='Password'
#     )

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'password']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         password = self.cleaned_data.get('password')
#         if password:
#             user.set_password(password)  # Update password only if provided
#         if commit:
#             user.save()
#         return user
