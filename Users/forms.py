from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation

from .models import *


class UserRegistrationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            "class": "form-control shadow-sm",
            'placeholder': 'Password'
        }),
        help_text=password_validation.password_validators_help_texts(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            "class": "form-control shadow-sm",
            'placeholder': 'Password confirmation'
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'password1', 'password2',
        )
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Username',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'E-Mail',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'First name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control shadow-sm',
                'placeholder': 'Last name',
                'required': True
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[
                self._meta.model.USERNAME_FIELD
            ].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)


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
        labels = {
            'about': 'About (Optional)'
        }


class UserAuthenticationForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': 'Username',
            'required': True
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control shadow-sm',
            'placeholder': 'Password',
            'required': True
        })
    )


class UpdateImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
        labels = {
            'image': 'Your image.'
        }
