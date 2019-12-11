from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings

import json
import os

from .models import Bot


class CreateBotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ('access_token',)
        widgets = {
            'access_token': forms.TextInput(attrs={'class': 'form-control'}),
        }


class GetAccessToken(forms.Form):
    access_token = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Access Token'}))
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}))
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telegram Nickname'}))


class TextForm(forms.Form):
    response_text = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Response Text', 'style': 'height: 80px'}))
    react_text = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'React Text'}))

    # def clean_react_text(self):
    #     new_react_text = self.cleaned_data['react_text']

    #     path = os.path.join(settings.BASE_DIR, 'BotConstructor',
    #                         'media', 'ScriptsBots', f'{request.user.username}_configuration.json')
    #     with open('configuration.json', 'r', encoding='utf-8') as file:
    #         object_text = json.load(file)['text']

    #     for item in object_text:
    #         if item['react_text'] == new_react_text:
    #             raise ValidationError(
    #                 f'Object "{new_react_text}" has already been created')

    #     return new_react_text


class ReplyMarkup(forms.Form):
    resize_keyboard = forms.BooleanField(
        label='Resize keyboard', required=False)
    one_time_keyboard = forms.BooleanField(
        label='One time keyboard', required=False)
    selective = forms.BooleanField(label='Selective', required=False)
    react_text = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'React Text'}))
    row_width = forms.IntegerField(max_value=5, widget=forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder': 'Row Width'}))
    response_text_markup = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Response Text'}))

    class Meta:
        widgets = {
            'resize_keyboard': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'one_time_keyboard': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'selective': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class ReplyButton(forms.Form):
    response_text = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Response Text'}))
    request_contact = forms.BooleanField(
        label='Request contact', required=False)
    request_location = forms.BooleanField(
        label='Request location', required=False)

    class Meta:
        widgets = {
            'request_contact': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'request_location': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
