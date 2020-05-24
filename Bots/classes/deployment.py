from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.conf import settings
from json import JSONDecodeError

import json
import os

from Bots.pythonanywhere import AutoDeploy
from Bots.functions import open_configuration


objects = {}


class RunBot(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'create_bot_third_step_url'

    def get(self, request, token: str):
        if token not in objects:
            deploy = AutoDeploy(
                file_title=f'{request.user.username}_{token}_test_bot.py')
            objects[token] = deploy
        else:
            deploy = objects[token]
        deploy.upload_file()

        try:
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
        except JSONDecodeError:
            messages.error(
                request,
                'Oooops... There is not consoles for hosting your bot'
            )
            return redirect(
                'create_bot_third_step_url',
                token=token
            )
        finally:
            del deploy
        return redirect('show_bots_url')


class StopBot(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'stop_bot_url'

    def get(self, request, token):
        path = open_configuration(request, token=token)
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        console_id = data['console_id']
        if token not in objects:
            deploy = AutoDeploy(
                file_title=f'{request.user.username}_{token}_test_bot.py')
            objects[token] = deploy
        else:
            deploy = objects[token]
        deploy.stop_bot(console_id=console_id)

        if 'count_deploys' in request.session.keys():
            del request.session['count_deploys']

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
        try:
            if token not in objects:
                deploy = AutoDeploy(
                    file_title=f'{request.user.username}_{token}_test_bot.py')
                objects[token] = deploy
            else:
                deploy = objects[token]
            deploy.run_bot(path)
        except JSONDecodeError:
            messages.error(
                request,
                'Oooops... There is not consoles for hosting your bot'
            )
            return redirect(
                'create_bot_third_step_url',
                token=token
            )
        request.session['count_deploys'] = 1

        messages.error(
            request,
            f'Bot, with token: {token} is running now'
        )
        return redirect('show_bots_url')


class RestartBot(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = "restart_bot"
    context = {}

    def get(self, request, token: str):
        path = open_configuration(request, token=token)
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        console_id = data['console_id']
        if token not in objects:
            deploy = AutoDeploy(
                file_title=f'{request.user.username}_{token}_test_bot.py')
            objects[token] = deploy
        else:
            deploy = objects[token]
        deploy.stop_bot(console_id=console_id)

        if 'count_deploys' in request.session.keys():
            del request.session['count_deploys']

        try:
            deploy.run_bot(path)
        except JSONDecodeError:
            messages.error(
                request,
                'Oooops... There is not consoles for hosting your bot'
            )
            return redirect(
                'create_bot_third_step_url',
                token=token
            )

        messages.error(
            request,
            f'Bot, with token: {token} was restarted.'
        )
        return redirect('show_bots_url')


class BotLogs(LoginRequiredMixin, View):
    login_url = '/signIn/'
    redirect_field_name = 'logs'

    def get(self, request, token):
        path = open_configuration(request, token)
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if 'console_id' in data.keys():
            log_path = os.path.join(
                settings.BASE_DIR, 'BotConstructor', 'media',
                'ScriptsBots', request.user.username,
                "{}_{}_output.log".format(
                    request.user.username, token.replace(':', '_'))
            )

            if token not in objects:
                deploy = AutoDeploy(
                    file_title=f'{request.user.username}_{token}_test_bot.py')
                objects[token] = deploy
            else:
                deploy = objects[token]
            deploy._write_to_log_file(
                request, token, data['console_id']
            )

            with open(log_path, 'r') as file_log:
                content = file_log.read()
        else:
            messages.error(request, 'Your bot is not hosting now')
            return redirect('show_bots_url')

        context = {
            'title': 'Logs - BotConstructor',
            'content': content,
            'token': token
        }
        return render(request, 'Logs.html', context)
