from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class UserRegistrationForm(forms.ModelForm):
    image = forms.FileField(required=False)
    password_some = forms.CharField(label='Password',
                                    widget=forms.PasswordInput(attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Password'
                                    }))
    password_confirm = forms.CharField(label='Confirm password',
                                       widget=forms.PasswordInput(attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Confirm password'
                                       }))
    about = forms.CharField(max_length=500, widget=forms.Textarea(attrs={
        'class': 'form-control mb-2 mt-2',
        'style': 'height: 100px', 'placeholder': 'About'
    }))

    class Meta:
        model = User
        fields = ('image', 'username', 'email', 'first_name', 'last_name',
                  'password_some', 'password_confirm')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-Mail'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            })
        }

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password_some")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords does not match")

        return cleaned_data


class UserAuthenticationForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UpdateImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
