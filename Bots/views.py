from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
import random
import json
import os

from .models import Profile, Bot
from .forms import GetAccessToken, CreateBotForm, TextForm, ReplyMarkup, ReplyButton
from .program import TextBuilder


data = {}


def open_configuration(request):
    path = os.path.join(settings.BASE_DIR, 'BotConstructor',
                        'media', 'ScriptsBots', f'{request.user.username}', f'{request.user.username}_configuration.json')
    if not os.path.exists(path):
        local_path = os.path.join(
            settings.BASE_DIR, 'BotConstructor', 'media', 'ScriptsBots', f'{request.user.username}')
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        path = os.path.join(
            local_path, f'{request.user.username}_configuration.json')
    return path


def open_test_bot(request):
    path = os.path.join(settings.BASE_DIR, 'BotConstructor',
                        'media', 'ScriptsBots', f'{request.user.username}', f'{request.user.username}_test_bot.py')
    if not os.path.exists(path):
        local_path = os.path.join(
            settings.BASE_DIR, 'BotConstructor', 'media', 'ScriptsBots', f'{request.user.username}')
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        path = os.path.join(local_path, f'{request.user.username}_test_bot.py')
    return path


def check_text_on_unique(request, text_element_1, text_element_2, index):
    path = open_configuration(request)
    with open(path, 'r', encoding='utf-8') as file:
        object_text = json.load(file)['text']

    for item in range(len(object_text)):
        if object_text[item]['react_text'] == text_element_1 and item == index and object_text[item]['response_text'] == text_element_2:
            messages.error(
                request, f'Object "{text_element_1}" has already been created')
            return False
    return True


class ShowBots(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'show_bots_url'

    def get(self, request):
        context = {
            'title': 'Your Bots - BotConstructor',
        }

        try:
            current_user_profile = Profile.objects.get(user=request.user)
            all_bots = Bot.objects.filter(owner=current_user_profile)
            if not all_bots:
                messages.error(request, 'No bots here')

            context.update({'all_bots': all_bots})
        except ObjectDoesNotExist:
            messages.error(request, 'Such user does not exist')

        return render(request, 'AllBots.html', context)


class UpdateBot(View):
    def get(self, request, bot_id):
        current_bot = Bot.objects.get(id=bot_id)
        update_bot_form = CreateBotForm(instance=current_bot)

        context = {
            'title': 'Update Bot - BotConstructor',
            'update_bot_form': update_bot_form
        }
        return render(request, 'UpdateBot.html', context)

    def post(self, request, bot_id):
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
    def get(self, request, bot_id):
        context = {
            'title': 'Delete Bot - BotConstructor'
        }
        return render(request, 'DeleteBot.html', context)

    def post(self, request, bot_id):
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
        try:
            path = open_configuration(request)
            with open(path, 'r', encoding='utf-8') as file:
                text_elements = list(enumerate(json.load(file)['text']))
        except KeyError:
            text_elements = []
        text_form = TextForm()

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'text_elements': text_elements,
            'text_form': text_form,
            'recognition_mark': 'text'
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request):
        try:
            path = open_configuration(request)
            with open(path, 'r', encoding='utf-8') as file:
                text_elements = list(enumerate(json.load(file)['text']))
        except KeyError:
            text_elements = []
        text_form = TextForm(request.POST)

        if text_form.is_valid():
            response_text = text_form.cleaned_data['response_text']
            react_text = text_form.cleaned_data['react_text'].strip()

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


class DeleteTextField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_text_url'

    def post(self, request, button_id):
        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        text_object = object_config['text']
        text_object.remove(text_object[button_id])

        object_config['text'] = text_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_text_url')


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
                if check_text_on_unique(request, final_data[0][1], final_data[1][1], final_data[0][0]):
                    text_object[item]['react_text'] = final_data[0][1].strip()
                    text_object[item]['response_text'] = final_data[1][1]

        object_config['text'] = text_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_text_url')


class CreateReplyMarkupField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'

    def get(self, request):
        try:
            path = open_configuration(request)
            with open(path, 'r', encoding='utf-8') as file:
                reply_markup_elements = list(
                    enumerate(json.load(file)['reply_markup']))
        except KeyError:
            reply_markup_elements = []

        reply_markup_form = ReplyMarkup()
        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_markup_form': reply_markup_form,
            'reply_markup_elements': reply_markup_elements,
            'recognition_mark': 'reply_markup'
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request):
        try:
            path = open_configuration(request)
            with open(path, 'r', encoding='utf-8') as file:
                reply_markup_elements = list(
                    enumerate(json.load(file)['reply_markup']))
        except KeyError:
            reply_markup_elements = []
        reply_markup_form = ReplyMarkup(request.POST)

        if reply_markup_form.is_valid():
            resize_keyboard = reply_markup_form.cleaned_data['resize_keyboard']
            one_time_keyboard = reply_markup_form.cleaned_data['one_time_keyboard']
            selective = reply_markup_form.cleaned_data['selective']
            react_text = reply_markup_form.cleaned_data['react_text']
            row_width = reply_markup_form.cleaned_data['row_width']
            response_text = reply_markup_form.cleaned_data['response_text_markup']

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
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    reply_markup_elements = list(
                        enumerate(json.load(file)['reply_markup']))
            except KeyError:
                reply_markup_elements = []
            return redirect('create_bot_second_step_reply_buttons_url')


class CreateReplyButtonsField(LoginRequiredMixin, View):
    context = {}
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_buttons_url'

    def get(self, request):
        try:
            path = open_configuration(request)
            with open(path, 'r', encoding='utf-8') as file:
                reply_markup_elements = list(
                    enumerate(json.load(file)['reply_markup']))
        except KeyError:
            reply_markup_elements = []
        reply_button_form = ReplyButton()

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'reply_button_form': reply_button_form,
            'reply_markup_elements': reply_markup_elements,
            'recognition_mark': 'reply_buttons'
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request):
        try:
            path = open_configuration(request)
            with open(path, 'r', encoding='utf-8') as file:
                reply_markup_elements = list(
                    enumerate(json.load(file)['reply_markup']))
        except KeyError:
            reply_markup_elements = []
        reply_button_form = ReplyButton(request.POST)

        if reply_button_form.is_valid():
            response_text = reply_button_form.cleaned_data['response_text']
            request_contact = reply_button_form.cleaned_data['request_contact']
            request_location = reply_button_form.cleaned_data['request_location']

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

            try:
                with open(path, 'r', encoding='utf-8') as file:
                    reply_markup_elements = list(
                        enumerate(json.load(file)['reply_markup']))
            except KeyError:
                reply_markup_elements = []

            self.context.update({
                'title': 'Second Step - BotConstructor',
                'reply_button_form': reply_button_form,
                'reply_markup_elements': reply_markup_elements,
                'recognition_mark': 'reply_buttons'
            })
            return render(request, 'SecondStep.html', self.context)


class DeleteReplyButtonField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'

    def post(self, request, markup_id, button_id):
        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        reply_button_object = object_config['reply_markup'][markup_id]['buttons']
        reply_button_object.remove(reply_button_object[button_id])

        object_config['reply_markup'][markup_id]['buttons'] = reply_button_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_reply_markup_url')


class DeleteReplyMarkupField(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_reply_markup_url'

    def post(self, request, markup_id):
        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        reply_markup_object = object_config['reply_markup']
        reply_markup_object.remove(reply_markup_object[markup_id])

        object_config['reply_markup'] = reply_markup_object
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(object_config, file, indent=4, ensure_ascii=False)
        return redirect('create_bot_second_step_reply_markup_url')


class GenerateFile(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_next_step_url'

    def get(self, request):
        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        program = TextBuilder(
            token=data['access_token'], user_username=str(request.user.username))
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

        program.reply_markup_response(
            reply_markup_dictionary=final_reply_markup_keyboard)
        program.text_response(text_dictionary=final_text_dictionary)
        program.polling_bot()

        file_script_path = 'ScriptBots/test_bot.py'
        file_config_path = 'ScriptBots/configuration.json'
        current_user = Profile.objects.get(user=request.user)
        access_token = data['access_token']

        bot_object = Bot(
            file_script=file_script_path, file_config=file_config_path, owner=current_user, access_token=access_token)
        bot_object.save()
        return redirect('create_bot_third_step_url')


class CreateBotStepTwo(View):
    @staticmethod
    @login_required
    def reply_markup_field_update(request):
        data = dict(request.POST)
        context = {}

        path = open_configuration(request)
        with open(path, 'r', encoding='utf-8') as file:
            object_config = json.load(file)

        text_object = object_config['reply_markup']
        final_data = []
        for button in data.items():
            index = button[0].split('_')
            # print(index)
            text = button[1][0]
            final_data.append([index, text])

        # print(final_data)

        # for item in range(len(text_object)):
        #     if item == final_data[0][0]:
        #         if check_text_on_unique(request, final_data[0][1], final_data[1][1], final_data[0][0]):
        #             text_object[item]['react_text'] = final_data[0][1].strip()
        #             text_object[item]['response_text'] = final_data[1][1]

        # object_config['text'] = text_object
        # with open('configuration.json', 'w', encoding='utf-8') as file:
        #     json.dump(object_config, file, indent=4, ensure_ascii=False)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reply_markup_elements = list(
                    enumerate(json.load(file)['reply_markup']))
        except KeyError:
            reply_markup_elements = []

        # context.update({
        #     'sub_recognition_mark': 'reply_buttons',
        #     'title': 'Second Step - BotConstructor',
        #     'reply_button_form': reply_button_form,
        #     'reply_markup_elements': reply_markup_elements,
        #     'recognition_mark': 'reply_markup'
        # })
        # return render(request, 'SecondStep.html', context)
        return redirect('create_bot_second_step_reply_markup_url')


class CreateBotStepThree(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_third_step_url'

    def get(self, request):
        context = {
            'title': 'Third Step - BotConstructor'
        }
        return render(request, 'ThirdStep.html', context)


class Download:
    @staticmethod
    @login_required
    def config(request):
        file_path = open_configuration(request)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response = HttpResponse(
                    file.read(), content_type='application/configuration.json')
                response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
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
                response['Content-Disposition'] = f'inline; filename={os.path.basename(file_path)}'
                return response
        return Http404
