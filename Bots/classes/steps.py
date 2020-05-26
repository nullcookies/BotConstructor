from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.http import JsonResponse

from ..functions import *
from ..forms import GetAccessToken
from ..models import Bot
from Users.models import Profile

import autopep8
import logging
import telebot


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
        data = {}

        if first_form.is_valid():
            access_token = first_form.cleaned_data['access_token']
            title = first_form.cleaned_data['title']
            username = first_form.cleaned_data['username']

            current_user_profile = Profile.objects.get(user=request.user)
            is_existed_bot = list(Bot.objects.filter(
                access_token=access_token,
                owner=current_user_profile
            ))
            if is_existed_bot != []:
                messages.error(
                    request, 'You already had bot with this token...')
                return redirect('show_bots_url')

            try:
                bot = telebot.TeleBot(
                    access_token
                )
                data.update({
                    'access_token': access_token,
                    'name': bot.get_me().first_name,
                    'username': bot.get_me().username
                })

                path = open_configuration(request, access_token)
                with open(path, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                return redirect(
                    'create_bot_second_step_text_url',
                    token=access_token
                )
            except Exception:
                messages.error(
                    request, 'Access token is not valid... '
                    'Try another... or wait for 3 minutes')

        context = {
            'title': 'First Step - BotConstructor',
            'first_form': first_form
        }
        return render(request, 'FirstStep.html', context)


# class UpdateAccessToken(LoginRequiredMixin, View):
#     login_url = '/signIn/'
#     redirect_field_name = 'create_bot_first_step_url'

#     def get(self, request, token: str):
#         path = open_configuration(request, token)
#         with open(path, 'r', encoding='utf8') as file:
#             data = json.load(file)

#         initial = {
#             'access_token': data['access_token'],
#             'title': data['name'],
#             'username': data['username']
#         }
#         first_form = GetAccessToken(initial=initial)

#         context = {
#             'title': 'First Step - BotConstructor',
#             'first_form': first_form
#         }
#         return render(request, 'FirstStep.html', context)

#     def post(self, request, token: str):
#         first_form = GetAccessToken(request.POST)

#         path = open_configuration(request, token)
#         with open(path, 'r', encoding='utf8') as file:
#             data = json.load(file)

#         if first_form.is_valid():
#             access_token: str = first_form.cleaned_data['access_token']
#             title: str = first_form.cleaned_data['title']
#             username: str = first_form.cleaned_data['username']

#             current_user_profile = Profile.objects.get(user=request.user)
#             is_existed_bot: list = list(Bot.objects.filter(
#                 access_token=access_token,
#                 owner=current_user_profile
#             ))
#             if is_existed_bot != [] and access_token != data['access_token']:
#                 messages.error(
#                     request, 'You already had bot with this token...')
#                 return redirect('show_bots_url')
#             try:
#                 bot = telebot.TeleBot(
#                     access_token
#                 )
#                 data = {
#                     'access_token': access_token,
#                     'name': bot.get_me().first_name,
#                     'username': bot.get_me().username
#                 }

#                 return redirect(
#                     'show_bots_url'
#                 )
#             except Exception:
#                 messages.error(
#                     request, 'Access token is not valid... '
#                     'Try another... or wait for 3 minutes')

#         context = {
#             'title': 'First Step - BotConstructor',
#             'first_form': first_form
#         }
#         return render(request, 'FirstStep.html', context)


class UntilFirstStep(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'until_first_step'

    def post(self, request):
        data = dict(request.POST)
        try:
            bot = telebot.TeleBot(data['token'][0])
            title = bot.get_me().first_name
            username = bot.get_me().username

            return JsonResponse({
                'title': title,
                'username': username,
                'csrfmiddlewaretoken': data['csrfmiddlewaretoken'],
                'button': True
            })
        except Exception:
            return JsonResponse({
                'button': False
            })


class CreateBotStepThree(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_third_step_url'

    def get(self, request, token: str):
        try:
            path = open_test_bot(request, token)
            with open(path, 'r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError as error:
            messages.error(request, 'No such bot...')
            return redirect('show_bots_url')

        config_path = open_configuration(request, token)
        base_name = os.path.basename(config_path)
        dir_name = os.path.basename(os.path.dirname(config_path))
        some = os.path.join(dir_name, base_name)
        print(some)

        context = {
            'title': 'Third Step - BotConstructor',
            'content': content,
            'token': token,
            'config': some
        }
        return render(request, 'ThirdStep.html', context)

    def post(self, request, token: str):
        data = dict(request.POST)
        code = data['code_editor'][0].replace('\r', '')

        path = open_test_bot(request, token)
        fixed_code = autopep8.fix_code(code)
        try:
            is_right_sliced = autopep8.check_syntax(code[:-30])
            exec(code[:-30])

            with open(path, 'w', encoding='utf-8') as file:
                file.write(fixed_code)
            return redirect(
                'create_bot_third_step_url',
                token=token
            )
        except (NameError, ValueError, TypeError, AttributeError,
                IndentationError) as error:
            messages.error(
                request,
                'You made a mistake in changing the program. '
                f'Current problem: {error}'
            )

        context = {
            'title': 'Third Step - BotConstructor',
            'content': fixed_code,
            'token': token
        }
        return render(request, 'ThirdStep.html', context)
