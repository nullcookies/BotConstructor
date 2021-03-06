from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.utils import timezone

import json
import os
import autopep8

from .models import Profile, Bot
from .program import BotFacade, TextBuilder, ReplyMarkupBuilder, \
    InlineMarkupBuilder, CallbackBuilder
from .forms import *
from .classes.text_field import *
from .classes.reply_markup_field import *
from .classes.reply_buttons_field import *
from .classes.inline_markup_field import *
from .classes.inline_buttons_field import *
from .functions import *
from .classes.steps import *
from .classes.callback import *
from .classes.tips import *


# Loading page
def loading_page(request):
    return render(request, 'PreloadingPage.html')


class ShowBots(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'show_bots_url'

    def get(self, request):
        context = {
            'title': 'Your Bots - BotConstructor',
        }

        try:
            current_user_profile = Profile.objects.get(user=request.user)
            all_bots = Bot.objects.filter(
                owner=current_user_profile).order_by('-date_created')
            if not all_bots:
                messages.error(request, 'No bots here')

            context.update({
                'all_bots': all_bots
            })
        except ObjectDoesNotExist:
            messages.error(request, 'Such user does not exist')

        return render(request, 'AllBots.html', context)


class DeleteBot(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'delete_bot_url'

    def get(self, request, bot_id: int, token: str):
        context = {
            'title': 'Delete Bot - BotConstructor'
        }
        return render(request, 'DeleteBot.html', context)

    def post(self, request, bot_id: int, token: str):
        current_bot = Bot.objects.get(id=bot_id)
        stop_hosting(current_bot)

        file_script_path = open_test_bot(request=request, token=token)
        file_config_path = open_configuration(request=request, token=token)

        os.remove(file_config_path)
        os.remove(file_script_path)

        try:
            file_logs_path = open_logs(request=request, token=token)
            os.remove(file_logs_path)
        except FileNotFoundError:
            pass

        if 'count_deploys' in request.session.keys():
            del request.session['count_deploys']

        current_bot.delete()
        return redirect('show_bots_url')


# TODO Rebuild system of using templates...
# class ShowTemplates(LoginRequiredMixin, View):
#     login_url = '/signIn/'
#     redirect_field_name = 'templates'
#     context = {}

#     def get(self, request, token: str):
#         template_form = ChooseTamplates()

#         self.context.update({
#             'title': 'Second Step - BotConstructor',
#             'template_form': template_form,
#             'token': token
#         })
#         return render(request, 'SecondStep.html', self.context)

#     def post(self, request, token: str):
#         template_form = ChooseTamplates(request.POST)

#         if template_form.is_valid():
#             current_bot_template = template_form.cleaned_data['templates']

#             path_template = os.path.join(settings.BASE_DIR, 'Bots',
#                                          'bot_templates',
#                                          f'{current_bot_template}.py')
#             with open(path_template, 'r', encoding='utf-8') as file:
#                 content = file.read()

#             path_config = open_configuration(request=request, token=token)
#             with open(path_config, 'r', encoding='utf-8') as file:
#                 access_token = json.load(file)['access_token']

#             current_user = Profile.objects.get(user=request.user)

#             bot_object = Bot(
#                 owner=current_user,
#                 access_token=access_token,
#                 title='NewsBot',
#                 username='NewsBotbot'
#             )
#             bot_object.save()

#             new_content = """
#             import telebot
#             from telebot.types import *


#             bot = telebot.TeleBot(token='{0}')
#             """.format(access_token)
#             content = new_content + content

#             fixed_code = autopep8.fix_code(content)
#             path = open_test_bot(request=request, token=token)
#             with open(path, 'w', encoding='utf-8') as file:
#                 file.write(fixed_code)
#             return redirect(
#                 'create_bot_third_step_url',
#                 token=token
#             )

#         self.context({
#             'title': 'Second Step - BotConstructor',
#             'template_form': template_form,
#             'token': token
#         })
#         return render(request, 'SecondStep.html', self.context)


class GenerateFile(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_second_step_next_step_url'

    def post(self, request, token: str):
        path = open_configuration(request, token)
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        point = False
        if 'text' in data and data['text'] != []:
            point = True
        elif 'reply_markup' in data and data['reply_markup'] != []:
            point = True
        elif 'inline_markup' in data and data['inline_markup'] != []:
            point = True
        elif 'callback' in data and data['callback'] != []:
            point = True

        if not point:
            messages.error(
                request,
                'You having empty configuration... Create some config!')
            return redirect('create_bot_second_step_text_url', token=token)

        username = str(request.user.username)
        text_builder = TextBuilder(token, username)
        reply_markup_builder = ReplyMarkupBuilder(token, username)
        inline_markup_builder = InlineMarkupBuilder(
            token, username)
        callback_builder = CallbackBuilder(token, username)

        program = BotFacade(text_builder, reply_markup_builder,
                            inline_markup_builder, callback_builder,
                            token, username, data, request)
        callback = program.operation()
        if callback is not None:
            messages.error(
                request,
                f'You have a problem buttons.' + callback[0]
            )
            if callback[1] == 'reply':
                return redirect(
                    'create_bot_second_step_reply_buttons_url',
                    token
                )
            else:
                return redirect(
                    'create_bot_second_step_inline_buttons_url',
                    token
                )

        some_path = open_test_bot(request=request, token=token)
        with open(some_path, 'r+', encoding='utf-8') as file:
            content_code = file.read()
            file.seek(0)
            file.truncate()
            file.write(content_code)

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
            bot_object = Bot(
                owner=current_user,
                access_token=access_token,
                title=data['name'],
                username=data['username'],
                date_created=timezone.now()
            )
            bot_object.file_script.save(
                f"{request.user.username}_{token.replace(':', '_')}"
                "_test_bot.py",
                File(open(file_script_path, encoding="utf8"))
            )
            bot_object.file_config.save(
                f"{request.user.username}_{token.replace(':', '_')}"
                "_configuration.json",
                File(open(file_config_path, encoding="utf8"))
            )
            bot_object.save()
        return redirect('create_bot_third_step_url', token=token)


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
                    file.read(), content_type='application/bot_script.py')
                response[
                    'Content-Disposition'
                ] = f'inline; filename={os.path.basename(file_path)}'
                return response
        return Http404

    @staticmethod
    @login_required
    def download_log(request, token: str):
        log_path = os.path.join(
            settings.BASE_DIR, 'BotConstructor', 'media',
            'ScriptsBots', request.user.username,
            "{}_{}_output.log".format(
                request.user.username, token.replace(':', '_'))
        )
        if os.path.exists(log_path):
            with open(log_path, 'rb') as file:
                response = HttpResponse(
                    file.read(), content_type='application/bot_output.log')
                response[
                    'Content-Disposition'
                ] = f'inline; filename={os.path.basename(log_path)}'
                return response
        return Http404
