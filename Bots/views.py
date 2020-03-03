from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.files import File

import json
import os
import autopep8

from .models import Profile, Bot
from .program import TextBuilder
from .forms import *
from .pythonanywhere import AutoDeploy
from .classes.text_field import *
from .classes.reply_markup_field import *
from .classes.reply_buttons_field import *
from .classes.inline_markup_field import *
from .classes.inline_buttons_field import *
from .functions import *
from .classes.steps import *
from .classes.callback import *


data = {}


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

            context.update({
                'all_bots': all_bots
            })
        except ObjectDoesNotExist:
            messages.error(request, 'Such user does not exist')

        return render(request, 'AllBots.html', context)


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


class ShowTemplates(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'templates'
    context = {}

    def get(self, request, token: str):
        template_form = ChooseTamplates()

        self.context.update({
            'title': 'Second Step - BotConstructor',
            'template_form': template_form,
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)

    def post(self, request, token: str):
        template_form = ChooseTamplates(request.POST)

        if template_form.is_valid():
            current_bot_template = template_form.cleaned_data['templates']

            path_template = os.path.join(settings.BASE_DIR, 'Bots',
                                         'bot_templates',
                                         f'{current_bot_template}.py')
            with open(path_template, 'r', encoding='utf-8') as file:
                content = file.read()

            path_config = open_configuration(request=request, token=token)
            with open(path_config, 'r', encoding='utf-8') as file:
                access_token = json.load(file)['access_token']

            new_content = """
            import telebot
            from telebot.types import *


            bot = telebot.TeleBot(token='{0}')
            """.format(access_token)
            content = new_content + content

            fixed_code = autopep8.fix_code(content)
            path = open_test_bot(request=request, token=token)
            with open(path, 'w', encoding='utf-8') as file:
                file.write(fixed_code)
            return redirect(
                'create_bot_third_step_url',
                token=token
            )

        self.context({
            'title': 'Second Step - BotConstructor',
            'template_form': template_form,
            'token': token
        })
        return render(request, 'SecondStep.html', self.context)


class GenerateFile(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_next_step_url'

    def get(self, request, token: str):
        path = open_configuration(request, token)
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        program = TextBuilder(token=data['access_token'],
                              user_username=str(request.user.username))

        try:
            final_text_dictionary = {}
            for text_element in data['text']:
                final_text_dictionary[
                    text_element['react_text']
                ] = [
                    text_element['response_text'],
                    text_element['remove_reply_markup']
                ]
            program.text_response(
                token=token, text_dictionary=final_text_dictionary)
        except KeyError as k_error:
            print(k_error)

        try:
            final_reply_markup_keyboard = {}
            for reply_markup_element in data['reply_markup']:
                buttons = []

                for button_element in reply_markup_element['buttons']:
                    buttons.append(
                        {
                            'response': button_element['response_text'],
                            'request_contact': button_element[
                                'request_contact'
                            ],
                            'request_location': button_element[
                                'request_location'
                            ]
                        }
                    )

                final_reply_markup_keyboard[
                    reply_markup_element['react_text']
                ] = {
                    'resize_keyboard': reply_markup_element['resize_keyboard'],
                    'one_time_keyboard': reply_markup_element[
                        'one_time_keyboard'
                    ],
                    'selective': reply_markup_element['selective'],
                    'row_width': reply_markup_element['row_width'],
                    'response_text': reply_markup_element['response_text'],
                    'buttons': buttons
                }
            program.reply_markup_response(
                reply_markup_dictionary=final_reply_markup_keyboard,
                token=token
            )
        except KeyError as k_error:
            k_error = str(k_error)

            message = ''
            if k_error == "'buttons'":
                message += ' You have not added buttons to the reply keyboard.'

                messages.error(
                    request,
                    f'You have a problem: {k_error}.' + message
                )
                return redirect(
                    'create_bot_second_step_reply_buttons_url',
                    token=token
                )

        try:
            final_inline_markup_keyboard = {}
            for inline_markup_element in data['inline_markup']:
                buttons = []

                for button_element in inline_markup_element['buttons']:
                    buttons.append(
                        {
                            'text': button_element['text'],
                            'url': button_element['url'],
                            'callback': button_element['callback'],
                            'switch_inline': button_element['switch_inline'],
                            'switch_inline_current': button_element[
                                'switch_inline_current'
                            ]
                        }
                    )

                final_inline_markup_keyboard[
                    inline_markup_element['react_text']
                ] = {
                    'row_width': inline_markup_element['row_width'],
                    'response_text': inline_markup_element['response_text'],
                    'buttons': buttons
                }
            program.inline_markup_response(
                inline_markup_dictionary=final_inline_markup_keyboard,
                token=token
            )
        except KeyError as k_error:
            k_error = str(k_error)

            message = ''
            if k_error == "'buttons'":
                message += (' You have not added buttons '
                            'to the inline keyboard.')

                messages.error(
                    request,
                    f'You have a problem: {k_error}.' + message
                )
                return redirect(
                    'create_bot_second_step_inline_buttons_url',
                    token=token
                )

        try:
            final_callback_query = {}
            for callback_element in data['callbacks']:
                for value_1, value_2, value_3 in zip(data['text'],
                                                     data['inline_markup'],
                                                     data['reply_markup']):
                    if callback_element['react_text'] == value_1['react_text']:
                        final_callback_query[
                            callback_element['callback']] = value_1
                    # elif callback_element[
                    #         'react_text'] == value_2['react_text']:
                    #     final_callback_query[
                    #         callback_element['callback']] = value_2
                    # elif callback_element[
                    #         'react_text'] == value_3['react_text']:
                    #     final_callback_query[
                    #         callback_element['callback']] = value_3
            print(final_callback_query, 'hi')

            program.callback_response(final_callback_query, token)
        except KeyError as k_error:
            print(k_error)

        program.polling_bot(token=token)

        some_path = open_test_bot(request=request, token=token)
        with open(some_path, 'r+', encoding='utf-8') as file:
            content_code = file.read()
            fixed_code = autopep8.fix_code(content_code)
            file.seek(0)
            file.truncate()
            file.write(fixed_code)

        file_script_path = open_test_bot(request=request, token=token)
        file_config_path = open_configuration(request=request, token=token)
        current_user = Profile.objects.get(user=request.user)
        access_token = data['access_token']

        current_user_profile = Profile.objects.get(user=request.user)
        is_existed_bot = list(Bot.objects.filter(
            access_token=access_token,
            owner=current_user_profile
        ))
        if is_existed_bot == []:
            bot_object = Bot(owner=current_user,
                             access_token=access_token, title=data['name'],
                             username=data['username'])
            bot_object.file_script.save(
                f"{request.user.username}_{token.replace(':', '_')}"
                "_test_bot.py",
                File(open(file_script_path))
            )
            bot_object.file_config.save(
                f"{request.user.username}_{token.replace(':', '_')}"
                "_configuration.py",
                File(open(file_config_path))
            )
            bot_object.save()

        path = open_test_bot(request, token)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        context = {
            'title': 'Third Step - BotConstructor',
            'content': content,
            'token': token
        }
        return render(request, 'ThirdStep.html', context)


class RunBot(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_third_step_url'

    def get(self, request, token: str):
        if 'count_deploys' in request.session.keys():
            if request.session['count_deploys'] <= 0:
                deploy = AutoDeploy(
                    file_title=f'{request.user.username}_{token}_test_bot.py')
                deploy.upload_file()
                console_id = deploy.create_console()
                deploy.open_console()
                deploy.send_input(console_id=console_id)

                path = open_configuration(request=request, token=token)
                with open(path, 'r+', encoding='utf-8') as file:
                    object_config = json.load(file)
                    object_config['console_id'] = console_id
                    file.seek(0)
                    json.dump(object_config, file,
                              indent=4, ensure_ascii=False)

                request.session['count_deploys'] = 1
                return redirect('show_bots_url')
            else:
                messages.error(request, 'You have already deployed your bot')
                return redirect(
                    'create_bot_third_step_url',
                    token=token
                )
        else:
            deploy = AutoDeploy(
                file_title=f'{request.user.username}_{token}_test_bot.py')
            deploy.upload_file()
            console_id = deploy.create_console()
            deploy.open_console()
            deploy.send_input(console_id=console_id)

            path = open_configuration(request=request, token=token)
            with open(path, 'r+', encoding='utf-8') as file:
                object_config = json.load(file)
                object_config['console_id'] = console_id
                file.seek(0)
                json.dump(object_config, file,
                          indent=4, ensure_ascii=False)

            request.session['count_deploys'] = 1
            return redirect('show_bots_url')


class StopBot(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'stop_bot_url'
    context = {}

    def get(self, request, token):
        path = open_configuration(request, token=token)
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        console_id = data['console_id']
        deploy = AutoDeploy(
            file_title=f'{request.user.username}_{token}_test_bot.py'
        )
        deploy.stop_bot(console_id=console_id)

        messages.error(
            request,
            f'Bot, with token: {token} has been stopped'
        )

        return redirect('show_bots_url')


class StartBot(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'stop_bot_url'
    context = {}

    def get(self, request, token):
        path = open_configuration(request, token=token)

        deploy = AutoDeploy(
            file_title=f'{request.user.username}_{token}_test_bot.py'
        )
        deploy.run_bot(path)

        messages.error(
            request,
            f'Bot, with token: {token} is running now'
        )
        return redirect('show_bots_url')


class Download:
    @staticmethod
    @login_required
    def config(request, token: str):
        file_path = open_configuration(request, token)
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
    def script(request, token: str):
        file_path = open_test_bot(request, token)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                response = HttpResponse(
                    file.read(), content_type='application/test_bot.py')
                response[
                    'Content-Disposition'
                ] = f'inline; filename={os.path.basename(file_path)}'
                return response
        return Http404
