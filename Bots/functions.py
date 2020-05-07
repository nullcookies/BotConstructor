import os
import json

from django.conf import settings
from django.contrib import messages
from .models import Bot
from .pythonanywhere import AutoDeploy


def open_configuration(request, token: str) -> str:
    token = token.replace(':', '_')
    path = os.path.join(settings.BASE_DIR, 'BotConstructor',
                        'media', 'ScriptsBots', f'{request.user.username}',
                        f'{request.user.username}_{token}_configuration.json')
    if not os.path.exists(path):
        local_path = os.path.join(
            settings.BASE_DIR, 'BotConstructor', 'media', 'ScriptsBots',
            f'{request.user.username}')
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        path = os.path.join(
            local_path, f'{request.user.username}_{token}_configuration.json')
    return path


def open_test_bot(request, token: str) -> str:
    token = token.replace(':', '_')
    path = os.path.join(settings.BASE_DIR, 'BotConstructor',
                        'media', 'ScriptsBots', f'{request.user.username}',
                        f'{request.user.username}_{token}_test_bot.py')
    if not os.path.exists(path):
        local_path = os.path.join(
            settings.BASE_DIR, 'BotConstructor', 'media', 'ScriptsBots',
            f'{request.user.username}')
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        path = os.path.join(
            local_path, f'{request.user.username}_{token}_test_bot.py')
    return path


def check_text_on_unique(request, text_element_1: str, text_element_2: str,
                         index: int, token: str) -> bool:
    path = open_configuration(request, token)
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


def enumerate_elements(request, get_object: str, token: str) -> list:
    try:
        path = open_configuration(request, token)
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


def stop_hosting(obj):
    file_name = str(obj.file_config).split('/')[1]
    name = file_name.split('_')[0]
    path = os.path.join(settings.BASE_DIR,
                        'BotConstructor', 'media', 'ScriptsBots',
                        name, file_name)

    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if 'console_id' in data:
        console_id = data['console_id']

        deploy = AutoDeploy(
            f'{obj.owner.user.username}_{obj.access_token}_test_bot.py'
        )
        deploy.stop_bot(console_id=console_id)
