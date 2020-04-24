from django.conf import settings
from abc import ABC, abstractmethod, abstractproperty
from telebot.types import *
from django.contrib import messages

import textwrap
import os
from django.shortcuts import redirect


PATH = os.path.join(settings.BASE_DIR, 'BotConstructor',
                    'media', 'ScriptsBots')


class BotFacade:
    def __init__(self, text_builder,
                 reply_markup_builder,
                 inline_markup_builder,
                 callback_builder,
                 token: str, user_username: str, data: dict) -> None:
        super().__init__()
        token = token.replace(':', '_')

        self.__token = token
        self.__username = user_username
        self._data = data

        self._text_builder = text_builder
        self._reply_markup_builder = reply_markup_builder
        self._inline_markup_builder = inline_markup_builder
        self._callback_builder = callback_builder

    def operation(self) -> None:
        self.__start()
        try:
            self._text_builder.create_option_dict(self._data['text'])
        except KeyError:
            pass

        try:
            self._reply_markup_builder.create_option_dict(
                self._data['reply_markup'])
        except KeyError:
            pass

        try:
            self._inline_markup_builder.create_option_dict(
                self._data['inline_markup'])
        except KeyError:
            pass

        try:
            self._callback_builder.create_option_dict(self._data['callbacks'])
        except KeyError:
            pass
        self.__end()

    def __start(self) -> None:
        init_object = f"""\
        import telebot
        from telebot.types import *

        bot = telebot.TeleBot(token='{self.__token}')

        """
        final_path = os.path.join(PATH, f'{self.__username}')
        path = os.path.join(
            final_path,
            f"{self.__username}_{self.__token}"
            "_test_bot.py"
        )
        with open(path, 'w', encoding='utf-8') as file:
            file.write(textwrap.dedent(init_object))

    def __end(self):
        polling_object = f"""
        bot.polling(none_stop=True)
        """

        final_path = os.path.join(PATH, f'{self.__username}')
        path = os.path.join(
            final_path, f'{self.__username}_{self.__token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(polling_object))


class TextBuilder:
    def __init__(self, token: str, username: str) -> None:
        super().__init__()
        self.__token = token.replace(':', '_')
        self.__username = username
        self.__text_dictionary = None

    def create_option_dict(self, data: list) -> None:
        try:
            if data != []:
                final_text_dictionary = {}
                for text_element in data:
                    final_text_dictionary[
                        text_element['react_text']
                    ] = [
                        text_element['response_text'],
                        text_element['remove_reply_markup']
                    ]
                self.__text_dictionary = final_text_dictionary
                self.__generate_text_code()
        except KeyError as k_error:
            print(k_error)

    def __generate_text_code(self) -> None:
        new_dict = {}
        for key, value in self.__text_dictionary.items():
            if self.__text_dictionary[key][1] is True:
                new_dict[key] = value

        for key in new_dict.keys():
            if key in self.__text_dictionary.keys():
                del self.__text_dictionary[key]

        object_text = """
        text_dictionary_messages = %s
        @bot.message_handler(func=lambda message: message.text \
in text_dictionary_messages.keys())
        def response_message(message):
            bot.send_message(chat_id=message.chat.id,
                            text=f'{text_dictionary_messages[message.text][0]}')

        """ % self.__text_dictionary

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

        final_path = os.path.join(PATH, f'{self.__username}')
        path = os.path.join(
            final_path, f'{self.__username}_{self.__token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))


class ReplyMarkupBuilder:
    def __init__(self, token: str, username: str, request) -> None:
        super().__init__()
        self.__token = token.replace(':', '_')
        self.__username = username
        self.__reply_markup_dictionary = None
        self.__request = request

    def create_option_dict(self, data: dict) -> None:
        try:
            if data != []:
                final_reply_markup_keyboard = {}
                for reply_markup_element in data:
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
                        'resize_keyboard': reply_markup_element[
                            'resize_keyboard'
                        ],
                        'one_time_keyboard': reply_markup_element[
                            'one_time_keyboard'
                        ],
                        'selective': reply_markup_element['selective'],
                        'row_width': reply_markup_element['row_width'],
                        'response_text': reply_markup_element['response_text'],
                        'buttons': buttons
                    }
                self.__reply_markup_dictionary = final_reply_markup_keyboard
                self.__generate_reply_code()
        except KeyError as k_error:
            k_error = str(k_error)

            message = ''
            if k_error == "'buttons'":
                message += ' You have not added buttons to the reply keyboard.'

                messages.error(
                    self.__request,
                    f'You have a problem: {k_error}.' + message
                )
                return redirect(
                    'create_bot_second_step_reply_buttons_url',
                    token=self.__token
                )

    def __generate_reply_code(self):
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

        """ % self.__reply_markup_dictionary

        final_path = os.path.join(PATH, f'{self.__username}')
        path = os.path.join(
            final_path, f'{self.__username}_{self.__token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))


class InlineMarkupBuilder:
    def __init__(self, token: str, username: str, request) -> None:
        super().__init__()
        self.__token = token.replace(':', '_')
        self.__username = username
        self.__inline_markup_dictionary = None
        self.__request = request

    def create_option_dict(self, data: dict) -> None:
        if data != []:
            final_inline_markup_keyboard = {}
            for inline_markup_element in data:
                buttons = []

                for button_element in inline_markup_element['buttons']:
                    buttons.append(
                        {
                            'text': button_element['text'],
                            'url': button_element['url'],
                            'callback': button_element['callback'],
                            'switch_inline': button_element[
                                'switch_inline'
                            ],
                            'switch_inline_current': button_element[
                                'switch_inline_current'
                            ]
                        }
                    )

                final_inline_markup_keyboard[
                    inline_markup_element['react_text']
                ] = {
                    'row_width': inline_markup_element['row_width'],
                    'response_text': inline_markup_element[
                        'response_text'
                    ],
                    'buttons': buttons
                }
            self.__inline_markup_dictionary = final_inline_markup_keyboard
            self.__generate_inline_code()

    def __generate_inline_code(self):
        try:
            object_text = """
            inline_markup_dictionary = %s
            @bot.message_handler(func=lambda message: message.text \
    in inline_markup_dictionary.keys())
            def response_inline(message):
                keyboard = InlineKeyboardMarkup(
                    row_width=inline_markup_dictionary[
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

            """ % self.__inline_markup_dictionary

            final_path = os.path.join(PATH, f'{self.__username}')
            path = os.path.join(
                final_path, f'{self.__username}_{self.__token}_test_bot.py')
            with open(path, 'a', encoding='utf-8') as file:
                file.write(textwrap.dedent(object_text))
        except KeyError as k_error:
            k_error = str(k_error)

            message = ''
            if k_error == "'buttons'":
                message += (' You have not added buttons '
                            'to the inline keyboard.')

                messages.error(
                    self.__request,
                    f'You have a problem: {k_error}.' + message
                )
                return redirect(
                    'create_bot_second_step_inline_buttons_url',
                    token=self.__token
                )


class CallbackBuilder:
    def __init__(self, token: str, username: str) -> None:
        super().__init__()
        self.__token = token.replace(':', '_')
        self.__username = username
        self.__callback_dictionary = None

    def create_option_dict(self, data: dict) -> None:
        try:
            if data != []:
                final_callback_query = {}
                for callback_element in data:
                    for value_1 in data['text']:
                        if callback_element['react_text'] == \
                                value_1['react_text']:
                            final_callback_query[
                                callback_element['callback']] = value_1
                self.__callback_dictionary = final_callback_query
                self.__generate_inline_code()
        except KeyError as k_error:
            print(k_error)

    def __generate_callback_code(self):
        object_text = ''
        for key, value in self.__callback_dictionary.items():
            object_text += """
                @bot.callback_query_handler(
                    func=lambda call: call.data == '%s' % '{0}'
                )
                def get_callback(call):
                    try:
                        bot.send_message(chat_id=call.from_user.id,
                                        text="%s" % '{1}')
                    except Exception as error:
                        pass

                """.format(key, value['response_text'])

        final_path = os.path.join(PATH, f'{self.__username}')
        path = os.path.join(
            final_path, f'{self.__username}_{self.__token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))
