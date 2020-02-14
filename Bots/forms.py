from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.conf import settings

import json
import os

from .models import Bot


CHECKBOX_CHOICES = (
    ('resize_keyboard', 'Resize Keyboard'),
    ('one_time_keyboard', 'One Time Keyboard'),
    ('selective', 'Selective')
)
CHOICES = (
    ('linkedin_mailer', 'Linked In Mailer'),
)
REPLY_BUTTONS_CHOICES = (
    ('request_contact', 'Request Contact'),
    ('request_location', 'Request Location')
)


class CreateBotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = ('access_token',)
        widgets = {
            'access_token': forms.TextInput(attrs={'class': 'form-control'}),
        }


class GetAccessToken(forms.Form):
    access_token = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Access Token'
    }))
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Title'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Telegram Nickname'
    }))


class TextForm(forms.Form):
    response_text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Response Text',
        'style': 'height: 80px'
    }))
    react_text = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'React Text'}))
    # command = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': 'Command'
    #         }
    #     )
    # )
    remove_reply_markup = forms.MultipleChoiceField(
        required=False, choices=(
            ('remove_reply', 'Remove Reply Markup'),
        ), widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(TextForm, self).__init__(*args, **kwargs)

    def clean_react_text(self):
        new_react_text = self.cleaned_data['react_text']

        path = os.path.join(settings.BASE_DIR, 'BotConstructor',
                            'media', 'ScriptsBots',
                            f'{self.request.user.username}',
                            f'{self.request.user.username}_configuration.json')
        try:
            with open(path, 'r', encoding='utf-8') as file:
                object_text = json.load(file)['text']

            for item in object_text:
                if item['react_text'] == new_react_text:
                    raise forms.ValidationError(
                        f'Object "{new_react_text}" has already been created')
        except KeyError as key:
            print(key)
        return new_react_text


class ReplyMarkup(forms.Form):
    checkboxes = forms.MultipleChoiceField(
        required=False, choices=CHECKBOX_CHOICES,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'custom-control-input'
            }
        )
    )
    react_text = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-2', 'placeholder': 'React Text'}))
    row_width = forms.IntegerField(max_value=5, min_value=1,
                                   widget=forms.NumberInput(attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Row Width'
                                   }))
    response_text_markup = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Response Text'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ReplyMarkup, self).__init__(*args, **kwargs)

    def clean_react_text(self):
        new_react_text = self.cleaned_data['react_text']

        path = os.path.join(settings.BASE_DIR, 'BotConstructor',
                            'media', 'ScriptsBots',
                            f'{self.request.user.username}',
                            f'{self.request.user.username}_configuration.json')
        try:
            with open(path, 'r', encoding='utf-8') as file:
                object_text = json.load(file)['reply_markup']

            for item in object_text:
                if item['react_text'] == new_react_text:
                    raise forms.ValidationError(
                        f'Object "{new_react_text}" has already been created')
        except KeyError as key:
            print(key)
        return new_react_text


class ReplyButton(forms.Form):
    response_text = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Response Text'}))
    radio_buttons = forms.CharField(
        widget=forms.RadioSelect(choices=REPLY_BUTTONS_CHOICES)
    )


class InlineMarkup(forms.Form):
    row_width = forms.IntegerField(max_value=5, min_value=1,
                                   widget=forms.NumberInput(attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Row Width'
                                   }))
    response_text = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Response Text'
    }))
    react_text = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'React Text'
    }))


class InlineButton(forms.Form):
    text = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Text'
    }))
    url = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Url'
    }))
    callback = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Callback Data'
    }), max_length=64, required=False)
    switch_inline = forms.CharField(required=False,
                                    widget=forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Switch Inline Query'
                                    }), max_length=50)
    switch_inline_current = forms.CharField(required=False,
                                            widget=forms.TextInput(attrs={
                                                'class': 'form-control',
                                                'placeholder': 'Switch Inline '
                                                               'Current Chat'
                                            }), max_length=50)

    def clean_url(self):
        new_url = self.cleaned_data['url']

        if new_url.strip() != '':
            validate = URLValidator()

            try:
                validate(new_url)
                return new_url
            except ValidationError:
                raise forms.ValidationError(f'URL {new_url} does not exist')
        else:
            return new_url


class ChooseTamplates(forms.Form):
    templates = forms.CharField(widget=forms.RadioSelect(choices=CHOICES))
