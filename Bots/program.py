from django.conf import settings
from abc import ABC, abstractmethod, abstractproperty
from telebot.types import *
from jinja2 import Template

import textwrap
import os


PATH = os.path.join(settings.BASE_DIR, 'BotConstructor',
                    'media', 'ScriptsBots')


class Builder(ABC):
    @abstractmethod
    def text_response(self) -> None:
        pass


class TextBuilder(Builder):
    def __init__(self, token, user_username):
        self.user_username = user_username
        init_object = f"""\
        import telebot
        from telebot.types import *

        bot = telebot.TeleBot(token='{token}')

        """
        final_path = os.path.join(PATH, f'{self.user_username}')
        path = os.path.join(
            final_path,
            f"{self.user_username}_{token.replace(':', '_')}_test_bot.py"
        )
        with open(path, 'w', encoding='utf-8') as file:
            file.write(textwrap.dedent(init_object))

    def text_response(self, text_dictionary: dict, token: str) -> None:
        token = token.replace(':', '_')

        new_dict = {}
        for key, value in text_dictionary.items():
            if text_dictionary[key][1] is True:
                new_dict[key] = value

        for key in new_dict.keys():
            if key in text_dictionary.keys():
                del text_dictionary[key]

        object_text = """
        text_dictionary_messages = %s
        @bot.message_handler(func=lambda message: message.text \
in text_dictionary_messages.keys())
        def response_message(message):
            print(text_dictionary_messages[message.text])
            bot.send_message(chat_id=message.chat.id,
                            text=f'{text_dictionary_messages[message.text][0]}',
                            reply_markup=ReplyKeyboardRemove())

        """ % text_dictionary

        for key, value in new_dict.items():
            object_text += textwrap.dedent(f"""
            @bot.message_handler(
                func=lambda message: message.text == '{key}'
            )
            def response_message_remove(message):
                bot.send_message(chat_id=message.chat.id,
                        text='{value[0]}',
                        reply_markup=ReplyKeyboardRemove())

            """)

        final_path = os.path.join(PATH, f'{self.user_username}')
        path = os.path.join(
            final_path, f'{self.user_username}_{token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))

    def reply_markup_response(self, reply_markup_dictionary: dict, token: str):
        token = token.replace(':', '_')

        object_text = """
        reply_markup_dictionary = %s
        @bot.message_handler(func=lambda message: message.text \
in reply_markup_dictionary.keys())
        def response_markup(message):
            keyboard = ReplyKeyboardMarkup(
                resize_keyboard=reply_markup_dictionary[message.text]['resize_keyboard'],
                one_time_keyboard=reply_markup_dictionary[message.text]['one_time_keyboard'],
                selective=reply_markup_dictionary[message.text]['selective'],
                row_width=reply_markup_dictionary[message.text]['row_width']
            )
            some_list = []

            for item in reply_markup_dictionary[message.text]['buttons']:
                button = KeyboardButton(text=f"{item['response']}",
                                        request_contact=item['request_contact'],
                                        request_location=item['request_location'])
                some_list.append(button)
            keyboard.add(*some_list)

            bot.send_message(chat_id=message.chat.id,
                             text=f"{reply_markup_dictionary[message.text]['response_text']}",
                             reply_markup=keyboard)

        """ % reply_markup_dictionary

        final_path = os.path.join(PATH, f'{self.user_username}')
        path = os.path.join(
            final_path, f'{self.user_username}_{token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))

    def inline_markup_response(self, inline_markup_dictionary: dict,
                               token: str):
        token = token.replace(':', '_')

        object_text = """
        inline_markup_dictionary = %s
        @bot.message_handler(func=lambda message: message.text \
in inline_markup_dictionary.keys())
        def response_inline(message):
            keyboard = InlineKeyboardMarkup(row_width=inline_markup_dictionary[
                message.text
            ]['row_width'])
            some_list = []

            for item in inline_markup_dictionary[message.text]['buttons']:
                generator_value = [
                    item[value] for value in item.keys()
                ]

                button = InlineKeyboardButton(*generator_value)
                some_list.append(button)
            keyboard.add(*some_list)

            bot.send_message(chat_id=message.chat.id,
                             text=f"{inline_markup_dictionary[message.text]['response_text']}",
                             reply_markup=keyboard)

        """ % inline_markup_dictionary

        final_path = os.path.join(PATH, f'{self.user_username}')
        path = os.path.join(
            final_path, f'{self.user_username}_{token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))

    def callback_response(self, callback_dictionary, token):
        token = token.replace(':', '_')

        object_text = ''
        for key, value in callback_dictionary.items():
            object_text += """
            @bot.callback_query_handler(
                func=lambda call: call.data == '%s' % '{0}'
            )
            def get_callback(call):
                try:
                    bot.send_message(chat_id=call.from_user.id,
                                     text="%s" % '{1}')

            """.format(key, value['response_text'])

        final_path = os.path.join(PATH, f'{self.user_username}')
        path = os.path.join(
            final_path, f'{self.user_username}_{token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))

    def polling_bot(self, token: str):
        token = token.replace(':', '_')

        polling_object = f"""
        bot.polling(none_stop=True)
        """

        final_path = os.path.join(PATH, f'{self.user_username}')
        path = os.path.join(
            final_path, f'{self.user_username}_{token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(polling_object))
