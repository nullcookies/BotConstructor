from django import template
from django.conf import settings

import os
import json

from ..pythonanywhere import get_status_of_console


register = template.Library()


@register.filter
def check_online(value: str):
    file_name = str(value).split('/')[1]
    name = file_name.split('_')[0]
    path = os.path.join(settings.BASE_DIR,
                        'BotConstructor', 'media', 'ScriptsBots',
                        name, file_name)

    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    if 'console_id' in data.keys():
        console_id = data['console_id']
        some_data = get_status_of_console(console_id)

        if some_data:
            return 'The bot is now running'
        else:
            return 'The bot was not launched'
    else:
        return 'The bot was not launched'
