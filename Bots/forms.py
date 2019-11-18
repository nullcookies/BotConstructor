from django import forms

from .models import Bot


class CreateBotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ('access_token', 'file_script')
        widgets = {
            'access_token': forms.TextInput(attrs={'class': 'form-control'}),
        }


class GetAccessToken(forms.Form):
    access_token = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Access Token'}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))


class TextForm(forms.Form):
    response_text = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Response Text'}))
    react_text = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'React Text'}))
