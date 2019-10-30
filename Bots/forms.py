from django import forms

from .models import Bot


class CreateBotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ('access_token', 'file_script')
        widgets = {
            'access_token': forms.TextInput(attrs={'class': 'form-control'}),
            'file_script': forms.TextInput(attrs={'class': 'form-control'}),
        }
