from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class UserRegistrationForm(forms.ModelForm):
    image = forms.FileField(required=False)
    password_some = forms.CharField(label='Password',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(label='Confirm password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('image', 'username', 'email', 'first_name', 'last_name',
                  'password_some', 'password_confirm')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        new_email = self.cleaned_data['email'].lower()

        if (new_email.startswith('example')) or (not (new_email.endswith('ru') or new_email.endswith('com') or new_email.endswith('net') or new_email.endswith('ua'))) or (not('gmail' in new_email or 'email' in new_email or 'mail' in new_email or 'ukr' in new_email)):
            raise ValidationError('Please, enter correct email address')

        return new_email

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get('password_some')
        confirm_password = cleaned_data.get('password_confirm')

        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')


class UserAuthenticationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UpdateImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
