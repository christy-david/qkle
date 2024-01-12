# forms.py

from django import forms
from django.contrib.auth.forms import UserChangeForm
from authentication.models import CustomUser
from django.core.exceptions import ValidationError

INPUT_CLASSES = 'block p-3 ps-5 appearance-none outline-none text-gray-900 text-sm font-medium w-full rounded placeholder-gray-900 border border-gray-900 mb-6'

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
          'first_name': forms.TextInput(attrs={
          'class': INPUT_CLASSES
          }),
          'last_name': forms.TextInput(attrs={
            'class': INPUT_CLASSES
          }),
          'username': forms.TextInput(attrs={
            'class': INPUT_CLASSES
          }),
          'email': forms.TextInput(attrs={
            'class': INPUT_CLASSES
          }),
        }

class UserEditForm(CustomUserChangeForm):
    def clean(self):
        cleaned_data = super().clean()
        new_username = cleaned_data.get('username')
        new_first_name = cleaned_data.get('first_name')
        new_last_name = cleaned_data.get('last_name')
        new_email = cleaned_data.get('email')

        # Check for empty username
        if not new_username:
            raise ValidationError('Username cannot be empty.')

        # Check for empty first name
        if not new_first_name:
            raise ValidationError('First name cannot be empty.')

        # Check for empty email
        if not new_email:
            raise ValidationError('Email cannot be empty.')

        # Check for duplicate username
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=new_username).exists():
            raise ValidationError('This username is already in use.')

        # Check for duplicate email
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=new_email).exists():
            raise ValidationError('This email address is already in use.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude the password field
        self.fields.pop('password', None)



