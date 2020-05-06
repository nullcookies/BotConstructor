from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class UserRegistrationForm(forms.ModelForm):
    password_some = forms.CharField(label='Password',
                                    widget=forms.PasswordInput(attrs={
                                        'class': 'form-control shadow-sm',
                                        'placeholder': 'Password'
                                    }))
    password_confirm = forms.CharField(label='Confirm password',
                                       widget=forms.PasswordInput(attrs={
                                           'class': 'form-control shadow-sm',
                                           'placeholder': 'Confirm password'
                                       }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'password_some', 'password_confirm')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'E-Mail',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
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


class UpdatingForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'E-Mail',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Last name'
            })
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('about',)
        widgets = {
            'about': forms.Textarea(attrs={
                'class': 'form-control shadow-sm',
                'style': 'height: 100px', 'placeholder': 'About'
            })
        }


class UserAuthenticationForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': 'Password'
        })
    )


class UpdateImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
        labels = {
            'image': 'Your image.'
        }
