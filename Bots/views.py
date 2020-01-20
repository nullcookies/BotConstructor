from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
# from pylint import epylint as lint

import random
import json
import os
# import pycodestyle

from .models import Profile, Bot
from .program import TextBuilder
from .forms import *


data = {}


def open_configuration(request) -> str:
    path = os.path.join(settings.BASE_DIR, 'BotConstructor',
                        'media', 'ScriptsBots', f'{request.user.username}',
                        f'{request.user.username}_configuration.json')
    if not os.path.exists(path):
        local_path = os.path.join(
            settings.BASE_DIR, 'BotConstructor', 'media', 'ScriptsBots',
            f'{request.user.username}')
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        path = os.path.join(
            local_path, f'{request.user.username}_configuration.json')
    return path


def open_test_bot(request) -> str:
    path = os.path.join(settings.BASE_DIR, 'BotConstructor',
                        'media', 'ScriptsBots', f'{request.user.username}',
                        f'{request.user.username}_test_bot.py')
    if not os.path.exists(path):
        local_path = os.path.join(
            settings.BASE_DIR, 'BotConstructor', 'media', 'ScriptsBots',
            f'{request.user.username}')
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        path = os.path.join(local_path, f'{request.user.username}_test_bot.py')
    return path


def check_text_on_unique(request, text_element_1: str, text_element_2: str,
                         index: int) -> bool:
    path = open_configuration(request)
    with open(path, 'r', encoding='utf-8') as file:
        object_text = json.load(file)['text']

    for item in range(len(object_text)):
        if object_text[item][
            'react_text'
        ] == text_element_1 and item == index and object_text[item][
            'response_text'
        ] == text_element_2:
            messages.error(
                request, f'Object "{text_element_1}" has already been created')
            return False
    return True


def enumerate_elements(request, get_object: str) -> list:
    try:
        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            elements = list(
                enumerate(json.load(file)[get_object]))
    except KeyError:
        elements = []
    return elements


def form_final_dict(obligatory_fields: list, index: int,
                    point: bool, data: dict, checkboxes: list = None) -> dict:
    final_data = {}
    for item in data.items():
        if item[0] != 'csrfmiddlewaretoken':
            if point:
                key = item[0][:item[0].rfind('_')]
            else:
                key = item[0][:item[0].rfind('_') - 2]

            if key in obligatory_fields:
                if checkboxes is not None and key in checkboxes and \
                        item[1][0] == 'on':
                    element = True
                else:
                    element = item[1][0]

                final_data[key] = [index, element]
                obligatory_fields.remove(key)

    for value in obligatory_fields:
        final_data[value] = [index, False]
    return final_data


class ShowBots(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'show_bots_url'

    def get(self, request):
        context = {
            'title': 'Your Bots - BotConstructor',
        }

        try:
            current_user_profile = Profile.objects.get(user=request.user)
            all_bots = Bot.objects.filter(owner=current_user_profile)[::-1]
            if not all_bots:
                messages.error(request, 'No bots here')

            context.update({'all_bots': all_bots})
        except ObjectDoesNotExist:
            messages.error(request, 'Such user does not exist')

        return render(request, 'AllBots.html', context)


class UpdateBot(View):
    def get(self, request, bot_id: int):
        current_bot = Bot.objects.get(id=bot_id)
        update_bot_form = CreateBotForm(instance=current_bot)

        context = {
            'title': 'Update Bot - BotConstructor',
            'update_bot_form': update_bot_form
        }
        return render(request, 'UpdateBot.html', context)

    def post(self, request, bot_id: int):
        current_bot = Bot.objects.get(id=bot_id)
        update_bot_form = CreateBotForm(
            request.POST, request.FILES, instance=current_bot)
        current_user = Profile.objects.get(user=request.user)

        if update_bot_form.is_valid():
            access_token = update_bot_form.cleaned_data['access_token']
            file = update_bot_form.cleaned_data['file_script']

            current_bot.access_token = access_token
            current_bot.file_script = file
            current_bot.owner = current_user
            current_bot.save()

            return redirect('show_bots_url')

        context = {
            'title': 'Update Bot - BotConstructor',
            'update_bot_form': update_bot_form
        }
        return render(request, 'UpdateBot.html', context)


class DeleteBot(View):
    def get(self, request, bot_id: int):
        context = {
            'title': 'Delete Bot - BotConstructor'
        }
        return render(request, 'DeleteBot.html', context)

    def post(self, request, bot_id: int):
        current_bot = Bot.objects.get(id=bot_id)
        current_bot.delete()
        return redirect('show_bots_url')


class CreateBotStepOne(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_first_step_url'

    def get(self, request):
        first_form = GetAccessToken()

        context = {
            'title': 'First Step - BotConstructor',
            'first_form': first_form
        }
        return render(request, 'FirstStep.html', context)

    def post(self, request):
        first_form = GetAccessToken(request.POST)

        if first_form.is_valid():
            access_token = first_form.cleaned_data['access_token']
            name = first_form.cleaned_data['name']
            username = first_form.cleaned_data['username']

            data.update({
                'access_token': access_token,
                'name': name,
                'username': username
            })

            path = open_configuration(request)
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            return redirect('create_bot_second_step_text_url')

        context = {
            'title': 'First Step - BotConstructor',
            'first_form': first_form
        }
        return render(request, 'FirstStep.html', context)


class CreateTextField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_text_url'

    def get(self, request):
        text_elements = enumerate_elements(request, get_object='text')
        text_form = TextForm(request=request)

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'text_elements': text_elements,
            'text_form': text_form,
            'recognition_mark': 'text'
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request):
        text_elements = enumerate_elements(request, get_object='text')
        text_form = TextForm(request.POST, request=request)

        if text_form.is_valid():
            response_text = text_form.cleaned_data['response_text']
            react_text = text_form.cleaned_data['react_text'].strip()

            path = open_configuration(request)
            with open(path, 'r+', encoding='utf-8') as file_name:
                object_config = json.load(file_name)

                try:
                    object_config['text'].append({
                        'response_text': response_text,
                        'react_text': react_text
                    })
                except KeyError:
                    object_config['text'] = [{
                        'response_text': response_text,
                        'react_text': react_text
                    }]
                file_name.seek(0)
                json.dump(object_config, file_name,
                          indent=4, ensure_ascii=False)
            return redirect('create_bot_second_step_text_url')

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'text_elements': text_elements,
            'text_form': text_form,
            'recognition_mark': 'text'
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateTextField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_text_url'

    def post(self, request):
        data = dict(request.POST)

        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        text_object = object_config['text']
        final_data = []
        for button in data.items():
            try:
                index = int(button[0].split('_')[-1])
                text = button[1][0]
                final_data.append([index, text])
            except ValueError:
                pass

        for item in range(len(text_object)):
            if item == final_data[0][0]:
                if check_text_on_unique(request, final_data[0][1],
                                        final_data[1][1], final_data[0][0]):
                    text_object[item]['react_text'] = final_data[0][1].strip()
                    text_object[item]['response_text'] = final_data[1][1]

        object_config['text'] = text_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_text_url')


class DeleteTextField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_text_url'

    def get(self, request, button_id: int):
        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        text_object = object_config['text']
        text_object.remove(text_object[button_id])

        object_config['text'] = text_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_text_url')


class CreateReplyMarkupField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'

    def get(self, request):
        reply_markup_elements = enumerate_elements(request,
                                                   get_object='reply_markup')
        reply_markup_form = ReplyMarkup(request=request)

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_markup_form': reply_markup_form,
            'reply_markup_elements': reply_markup_elements,
            'recognition_mark': 'reply_markup'
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request):
        reply_markup_elements = enumerate_elements(request,
                                                   get_object='reply_markup')
        reply_markup_form = ReplyMarkup(request.POST, request=request)

        if reply_markup_form.is_valid():
            resize_keyboard = reply_markup_form.cleaned_data['resize_keyboard']
            one_time_keyboard = reply_markup_form.cleaned_data[
                'one_time_keyboard'
            ]
            selective = reply_markup_form.cleaned_data['selective']
            react_text = reply_markup_form.cleaned_data['react_text']
            row_width = reply_markup_form.cleaned_data['row_width']
            response_text = reply_markup_form.cleaned_data[
                'response_text_markup'
            ]

            path = open_configuration(request)
            with open(path, 'r+', encoding='utf-8') as file_name:
                object_config = json.load(file_name)

                try:
                    object_config['reply_markup'].append({
                        'resize_keyboard': resize_keyboard,
                        'one_time_keyboard': one_time_keyboard,
                        'selective': selective,
                        'react_text': react_text,
                        'row_width': row_width,
                        'response_text': response_text
                    })
                except KeyError:
                    object_config['reply_markup'] = [{
                        'resize_keyboard': resize_keyboard,
                        'one_time_keyboard': one_time_keyboard,
                        'selective': selective,
                        'react_text': react_text,
                        'row_width': row_width,
                        'response_text': response_text
                    }]
                file_name.seek(0)
                json.dump(object_config, file_name,
                          indent=4, ensure_ascii=False)

            reply_markup_elements = enumerate_elements(request,
                                                       'reply_markup')
            return redirect('create_bot_second_step_reply_buttons_url')

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_markup_form': reply_markup_form,
            'reply_markup_elements': reply_markup_elements,
            'recognition_mark': 'reply_markup'
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateReplyMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'

    checkboxes = [
        'resize_keyboard',
        'one_time_keyboard',
        'selective'
    ]

    def post(self, request):
        obligatory_fields = [
            'resize_keyboard',
            'one_time_keyboard',
            'selective',
            'react_text',
            'row_width',
            'response_text_markup'
        ]
        data = dict(request.POST)

        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        index = int(list(data.items())[1][0].split('_')[-1])
        final_data = form_final_dict(obligatory_fields=obligatory_fields,
                                     point=True, checkboxes=self.checkboxes,
                                     index=index, data=data)

        reply_markup_object = object_config['reply_markup']

        reply_markup_object[index]['react_text'] = final_data[
            'react_text'
        ][1].strip()
        reply_markup_object[index]['row_width'] = int(
            final_data['row_width'][1].strip())
        reply_markup_object[index]['response_text'] = final_data[
            'response_text_markup'
        ][1].strip()
        reply_markup_object[index]['resize_keyboard'] = final_data[
            'resize_keyboard'
        ][1]
        reply_markup_object[index]['one_time_keyboard'] = final_data[
            'one_time_keyboard'
        ][1]
        reply_markup_object[index]['selective'] = final_data['selective'][1]

        object_config['reply_markup'] = reply_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_reply_markup_url')


class DeleteReplyMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'

    def get(self, request, markup_id):
        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        reply_markup_object = object_config['reply_markup']
        reply_markup_object.remove(reply_markup_object[markup_id])

        object_config['reply_markup'] = reply_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_reply_markup_url')


class CreateReplyButtonsField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_buttons_url'

    def get(self, request):
        reply_markup_elements = enumerate_elements(request,
                                                   get_object='reply_markup')
        reply_button_form = ReplyButton()

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_button_form': reply_button_form,
            'reply_markup_elements': reply_markup_elements,
            'recognition_mark': 'reply_buttons'
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request):
        reply_markup_elements = enumerate_elements(request,
                                                   get_object='reply_markup')
        reply_button_form = ReplyButton(request.POST)

        if reply_button_form.is_valid():
            response_text = reply_button_form.cleaned_data[
                'response_text'
            ]
            request_contact = reply_button_form.cleaned_data[
                'request_contact'
            ]
            request_location = reply_button_form.cleaned_data[
                'request_location'
            ]

            path = open_configuration(request)
            with open(path, 'r+', encoding='utf-8') as file_name:
                object_config = json.load(file_name)

                try:
                    object_config['reply_markup'][-1]['buttons'].append({
                        'response_text': response_text,
                        'request_contact': request_contact,
                        'request_location': request_location
                    })
                except KeyError:
                    object_config['reply_markup'][-1]['buttons'] = [{
                        'response_text': response_text,
                        'request_contact': request_contact,
                        'request_location': request_location
                    }]
                file_name.seek(0)
                json.dump(object_config, file_name,
                          indent=4, ensure_ascii=False)
                return redirect('create_bot_second_step_reply_buttons_url')

        reply_markup_elements = enumerate_elements(request, 'reply_markup')
        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_button_form': reply_button_form,
            'reply_markup_elements': reply_markup_elements,
            'recognition_mark': 'reply_buttons'
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateReplyButtonsField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_buttons_url'

    checkboxes = [
        'request_contact',
        'request_location'
    ]

    def post(self, request):
        data = dict(request.POST)
        obligatory_fields = [
            'response_text',
            'request_contact',
            'request_location'
        ]

        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        index = (int(list(data.items())[1][0].split('_')[-2]),
                 int(list(data.items())[1][0].split('_')[-1]))
        final_data = form_final_dict(obligatory_fields=obligatory_fields,
                                     point=False, checkboxes=self.checkboxes,
                                     index=index, data=data)

        reply_markup_object = object_config['reply_markup']
        reply_markup_object[index[0]]['buttons'][index[1]][
            'response_text'
        ] = final_data['response_text'][1].strip()
        reply_markup_object[index[0]]['buttons'][index[1]][
            'request_contact'
        ] = final_data['request_contact'][1]
        reply_markup_object[index[0]]['buttons'][index[1]][
            'request_location'
        ] = final_data['request_location'][1]

        object_config['reply_markup'] = reply_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_reply_buttons_url')


class DeleteReplyButtonField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'

    def get(self, request, markup_id: int, button_id: int):
        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        reply_button_object = object_config[
            'reply_markup'
        ][markup_id]['buttons']
        reply_button_object.remove(reply_button_object[button_id])

        object_config[
            'reply_markup'
        ][markup_id]['buttons'] = reply_button_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_reply_markup_url')


class CreateInlineMarkupField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'

    def get(self, request):
        inline_markup_elements = enumerate_elements(request,
                                                    get_object='inline_markup')
        inline_markup_form = InlineMarkup()
        self.context.update({
            'title': 'Second Step - BotConstructor',
            'inline_markup_form': inline_markup_form,
            'inline_markup_elements': inline_markup_elements,
            'recognition_mark': 'inline_markup'
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request):
        inline_markup_elements = enumerate_elements(request,
                                                    get_object='inline_markup')
        inline_markup_form = InlineMarkup(request.POST)

        if inline_markup_form.is_valid():
            row_width = inline_markup_form.cleaned_data['row_width']
            response_text = inline_markup_form.cleaned_data['response_text']
            react_text = inline_markup_form.cleaned_data['react_text']

            path = open_configuration(request)
            with open(path, 'r+', encoding='utf-8') as file:
                object_config = json.load(file)

                try:
                    object_config['inline_markup'].append({
                        'row_width': row_width,
                        'response_text': response_text,
                        'react_text': react_text
                    })
                except KeyError:
                    object_config['inline_markup'] = [{
                        'row_width': row_width,
                        'react_text': react_text,
                        'response_text': response_text
                    }]
                file.seek(0)
                json.dump(object_config, file,
                          indent=4, ensure_ascii=False)
                return redirect('create_bot_second_step_inline_markup_url')

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'inline_markup_form': inline_markup_form,
            'inline_markup_elements': inline_markup_elements,
            'recognition_mark': 'inline_markup'
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateInlineMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'

    def post(self, request):
        data = dict(request.POST)
        print(data)

        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        inline_markup_object = object_config['inline_markup']
        final_data = []
        index = int(list(data.items())[1][0].split('_')[-1])

        for inline_markup in data.items():
            if inline_markup[0] != 'csrfmiddlewaretoken':
                text = inline_markup[1][0]
                final_data.append([index, text])

        for item in range(len(inline_markup_object)):
            if item == index:
                # if check_text_on_unique(request, final_data[0][1],
                #                         final_data[1][1], final_data[0][0]):
                inline_markup_object[item][
                    'react_text'
                ] = final_data[1][1].strip()
                inline_markup_object[item][
                    'response_text'
                ] = final_data[0][1].strip()
                inline_markup_object[item]['row_width'] = final_data[2][1]

        object_config['inline_markup'] = inline_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)

        return redirect('create_bot_second_step_inline_markup_url')


class DeleteInlineMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'

    def get(self, request, markup_id):
        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        reply_markup_object = object_config['inline_markup']
        reply_markup_object.remove(reply_markup_object[markup_id])

        object_config['inline_markup'] = reply_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_inline_markup_url')


class CreateInlineButtonsField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'

    def get(self, request):
        inline_markup_elements = enumerate_elements(request,
                                                    get_object='inline_markup')
        inline_button_form = InlineButton()

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'inline_button_form': inline_button_form,
            'inline_markup_elements': inline_markup_elements,
            'recognition_mark': 'inline_buttons'
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request):
        inline_markup_elements = enumerate_elements(request,
                                                    get_object='inline_markup')
        inline_button_form = InlineButton(request.POST)

        if inline_button_form.is_valid():
            text = inline_button_form.cleaned_data['text']
            url = inline_button_form.cleaned_data['url']
            callback = inline_button_form.cleaned_data['callback']
            switch_inline = inline_button_form.cleaned_data['switch_inline']
            switch_inline_current = inline_button_form.cleaned_data[
                'switch_inline_current'
            ]
            print(text, url, callback, switch_inline, switch_inline_current)

            path = open_configuration(request)
            with open(path, 'r+', encoding='utf-8') as file:
                object_config = json.load(file)

                try:
                    object_config['inline_markup'][-1][
                        'buttons'
                    ].append({
                        'text': text,
                        'url': url,
                        'callback': callback,
                        'switch_inline': switch_inline,
                        'switch_inline_current': switch_inline_current
                    })
                except KeyError:
                    object_config['inline_markup'][-1]['buttons'] = [{
                        'text': text,
                        'url': url,
                        'callback': callback,
                        'switch_inline': switch_inline,
                        'switch_inline_current': switch_inline_current
                    }]
                file.seek(0)
                json.dump(object_config, file,
                          indent=4, ensure_ascii=False)
                return redirect('create_bot_second_step_inline_buttons_url')

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'inline_button_form': inline_button_form,
            'inline_markup_elements': inline_markup_elements,
            'recognition_mark': 'inline_buttons'
        })
        return render(request, 'SecondStep.html', self.context)


class UpdateInlineMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_buttons_url'

    def post(self, request):
        data = dict(request.POST)
        print(data)

        obligatory_fields = [
            'text_inline',
            'url_inline',
            'callback',
            'switch_inline',
            'switch_inline_current'
        ]

        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        index = (int(list(data.items())[1][0].split('_')[-2]),
                 int(list(data.items())[1][0].split('_')[-1]))
        final_data = form_final_dict(obligatory_fields=obligatory_fields,
                                     point=False, index=index, data=data)

        inline_markup_object = object_config['inline_markup']
        print(inline_markup_object)
        inline_markup_object[index[0]]['buttons'][index[1]][
            'text'
        ] = final_data['text_inline'][1].strip()
        inline_markup_object[index[0]]['buttons'][index[1]][
            'url'
        ] = final_data['url_inline'][1]
        inline_markup_object[index[0]]['buttons'][index[1]][
            'callback'
        ] = final_data['callback'][1]
        inline_markup_object[index[0]]['buttons'][index[1]][
            'switch_inline'
        ] = final_data['switch_inline'][1]
        inline_markup_object[index[0]]['buttons'][index[1]][
            'switch_inline_current'
        ] = final_data['switch_inline_current'][1]

        object_config['inline_markup'] = inline_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_inline_buttons_url')


class DeleteInlineButtonField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_inline_markup_url'

    def get(self, request, markup_id: int, button_id: int):
        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        inline_button_object = object_config[
            'inline_markup'
        ][markup_id]['buttons']
        inline_button_object.remove(inline_button_object[button_id])

        object_config[
            'inline_markup'
        ][markup_id]['buttons'] = inline_button_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_inline_markup_url')


class GenerateFile(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_next_step_url'

    def get(self, request):
        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        program = TextBuilder(token=data['access_token'],
                              user_username=str(request.user.username))
        final_text_dictionary = {}
        for text_element in data['text']:
            final_text_dictionary[text_element['react_text']
                                  ] = text_element['response_text']

        final_reply_markup_keyboard = {}
        for reply_markup_element in data['reply_markup']:
            buttons = []

            for button_element in reply_markup_element['buttons']:
                buttons.append(
                    {
                        'response': button_element['response_text'],
                        'request_contact': button_element['request_contact'],
                        'request_location': button_element['request_location']
                    }
                )

            final_reply_markup_keyboard[reply_markup_element['react_text']] = {
                'resize_keyboard': reply_markup_element['resize_keyboard'],
                'one_time_keyboard': reply_markup_element['one_time_keyboard'],
                'selective': reply_markup_element['selective'],
                'row_width': reply_markup_element['row_width'],
                'response_text': reply_markup_element['response_text'],
                'buttons': buttons
            }

        program.text_response(text_dictionary=final_text_dictionary)
        program.reply_markup_response(
            reply_markup_dictionary=final_reply_markup_keyboard)
        program.polling_bot()

        file_script_path = 'ScriptBots/test_bot.py'
        file_config_path = 'ScriptBots/configuration.json'
        current_user = Profile.objects.get(user=request.user)
        access_token = data['access_token']

        bot_object = Bot(file_script=file_script_path,
                         file_config=file_config_path, owner=current_user,
                         access_token=access_token, title=data['name'],
                         username=data['username'])
        bot_object.save()
        return redirect('create_bot_third_step_url')


class CreateBotStepThree(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_third_step_url'

    def get(self, request):
        path = open_test_bot(request)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()

        context = {
            'title': 'Third Step - BotConstructor',
            'content': content
        }
        return render(request, 'ThirdStep.html', context)

    def post(self, request):
        data = dict(request.POST)
        code = data['code_editor'][0].replace('\r', '')

        path = open_test_bot(request)
        # pylint_stdout, pylint_stderr = lint.py_run(path, return_std=True)
        # print(pylint_stdout, pylint_stderr)
        # some = pycodestyle.Checker(filename=path).run_check()
        # print(some)
        with open(path, 'w', encoding='utf-8') as file:
            file.write(code)

        return redirect('create_bot_third_step_url')


class Download:
    @staticmethod
    @login_required
    def config(request):
        file_path = open_configuration(request)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response = HttpResponse(
                    file.read(), content_type='application/configuration.json')
                response[
                    'Content-Disposition'
                ] = f'inline; filename={os.path.basename(file_path)}'
                return response
        return Http404

    @staticmethod
    @login_required
    def script(request):
        file_path = open_test_bot(request)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response = HttpResponse(
                    file.read(), content_type='application/test_bot.py')
                response[
                    'Content-Disposition'
                ] = f'inline; filename={os.path.basename(file_path)}'
                return response
        return Http404
