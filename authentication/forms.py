from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from authentication.models import CustomUser


sign_up_form_class='block p-3 ps-5 appearance-none outline-none text-gray-900 text-sm font-medium w-full rounded placeholder-gray-900 border border-gray-900 mb-6'
log_in_form_class='block p-3 ps-5 appearance-none outline-none text-gray-900 text-sm font-medium w-full rounded placeholder-gray-900 border border-gray-900 mb-6'
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': log_in_form_class
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': log_in_form_class
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')
    
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': sign_up_form_class
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': sign_up_form_class
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': sign_up_form_class
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class': sign_up_form_class
    }))