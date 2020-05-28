from django.conf import settings
from abc import ABC, abstractmethod, abstractproperty
from telebot.types import *
from django.contrib import messages
from django.shortcuts import redirect

import textwrap
import os


PATH = os.path.join(settings.BASE_DIR, 'BotConstructor',
                    'media', 'ScriptsBots')


class BotFacade:
    def __init__(self, text_builder,
                 reply_markup_builder,
                 inline_markup_builder,
                 callback_builder,
                 token: str, user_username: str,
                 data: dict, request) -> None:
        super().__init__()
        token = token.replace(':', '_')

        self.__token = token
        self.__username = user_username
        self.__request = request
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
            reply_callback = self._reply_markup_builder.create_option_dict(
                self._data['reply_markup'])
            if reply_callback is not None:
                return reply_callback, 'reply'
        except KeyError:
            pass

        try:
            inline_callback = self._inline_markup_builder.create_option_dict(
                self._data['inline_markup'])
            if inline_callback is not None:
                return inline_callback, 'inline'
        except KeyError:
            pass

        try:
            self._callback_builder.create_option_dict(self._data)
        except KeyError:
            pass
        self.__end()

    def __start(self) -> None:
        some_token = self.__token.replace('_', ':', 1)
        init_object = textwrap.dedent(f"""\
        import telebot
        import requests
        import logging
        import os
        import sys

        from telebot.types import *
        from fuzzywuzzy import fuzz

        bot = telebot.TeleBot(token='{some_token}')
        logger = telebot.logger
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s => %(message)s'
        )
        ch = logging.StreamHandler(sys.stdout)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
        ch.setFormatter(formatter)


        def generate_synonyms(word: str) -> None:
            url = f'https://api.datamuse.com/words?rel_syn=%s' % word
            phrase = dict()

            response = requests.get(url)
            if response.status_code <= 200:
                synonyms = response.json()

                for element in synonyms:
                    if word not in phrase:
                        phrase[word] = [element['word']]
                    else:
                        phrase[word].append(element['word'])
                try:
                    phrase[word].append(word)
                except KeyError:
                    phrase[word] = [word]
            return phrase

        """)
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
                        text_element['remove_reply_markup'],
                        text_element['smart']
                    ]
                self.__text_dictionary = final_text_dictionary
                self.__generate_text_code()
        except KeyError as k_error:
            print(k_error)

    def __generate_text_code(self) -> None:
        new_dict = {}
        smart_texts = {}
        object_text = ""

        for key, value in self.__text_dictionary.items():
            if self.__text_dictionary[key][1] is True:
                new_dict[key] = value

            if self.__text_dictionary[key][2] is True:
                smart_texts[key] = value

        for key in new_dict.keys():
            if key in self.__text_dictionary.keys():
                del self.__text_dictionary[key]

        for key in smart_texts.keys():
            if key in self.__text_dictionary.keys():
                del self.__text_dictionary[key]

            if key in new_dict.keys():
                del new_dict[key]

        if self.__text_dictionary:
            object_text += textwrap.dedent("""
            text_dictionary = %s
            @bot.message_handler(
                func=lambda message: message.text in text_dictionary.keys()
            )
            def response_message(message):
                logger.info(
                    "User -> {user_message} : Bot -> {bot_message}".format(
                        user_message=message.text,
                        bot_message=(text_dictionary[message.text][0]).replace(
                            '\\n', ''
                        )
                    )
                )
                try:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=f'{text_dictionary[message.text][0]}'.format(
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            is_bot=message.from_user.is_bot,
                            id=message.from_user.id,
                            message_id=message.message_id
                        ),
                        parse_mode='Markdown'
                    )
                except telebot.apihelper.ApiException:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=f'{text_dictionary[message.text][0]}'.format(
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            is_bot=message.from_user.is_bot,
                            id=message.from_user.id,
                            message_id=message.message_id
                        )
                    )

            """) % self.__text_dictionary

        for key, value in new_dict.items():
            object_text += textwrap.dedent("""
            @bot.message_handler(
                func=lambda message: message.text == %s
            )
            def response_message_remove(message):
                logger.info(
                    "User -> {user_message} : Bot -> {bot_message}".format(
                        user_message=message.text,
                        bot_message=%s.replace(
                            '\\n', ''
                        )
                    )
                )
                try:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=%s.format(
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            is_bot=message.from_user.is_bot,
                            id=message.from_user.id,
                            message_id=message.message_id
                        ),
                        reply_markup=ReplyKeyboardRemove(),
                        parse_mode='Markdown'
                    )
                except telebot.apihelper.ApiException:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=%s.format(
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            is_bot=message.from_user.is_bot,
                            id=message.from_user.id,
                            message_id=message.message_id
                        ),
                        reply_markup=ReplyKeyboardRemove()
                    )
            """ % (repr(key), repr(value[0]), repr(value[0]), repr(value[0])))

        for key, value in smart_texts.items():
            object_text += textwrap.dedent("""
            def check_similarity_%s(word: Message) -> dict:
                generated_phrases = generate_synonyms(%s.lower())

                word = word.text
                params = {'word': '', 'percent': 0}

                for value in generated_phrases[%s.lower()]:
                    similarity = fuzz.ratio(word, value)
                    if similarity >= params[
                            'percent'] and similarity >= 60:
                        params['word'] = value
                        params['percent'] = similarity
                return True if params['percent'] != 0 else False


            @bot.message_handler(func=check_similarity_%s)
            def handler(message: Message) -> None:
                logger.info(
                    "User -> {user_message} : Bot -> {bot_message}".format(
                        user_message=message.text,
                        bot_message=%s.replace(
                            '\\n', ''
                        )
                    )
                )
                if %s:
                    try:
                        bot.send_message(
                            chat_id=message.chat.id,
                            text=%s.format(
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                is_bot=message.from_user.is_bot,
                                id=message.from_user.id,
                                message_id=message.message_id
                            ),
                            reply_markup=ReplyKeyboardRemove(),
                            parse_mode='Markdown'
                        )
                    except telebot.apihelper.ApiException:
                        bot.send_message(
                            chat_id=message.chat.id,
                            text=%s.format(
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                is_bot=message.from_user.is_bot,
                                id=message.from_user.id,
                                message_id=message.message_id
                            ),
                            reply_markup=ReplyKeyboardRemove(),
                            parse_mode='Markdown'
                        )
                else:
                    try:
                        bot.send_message(
                            chat_id=message.chat.id,
                            text=%s.format(
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                is_bot=message.from_user.is_bot,
                                id=message.from_user.id,
                                message_id=message.message_id
                            ),
                            parse_mode='Markdown'
                        )
                    except telebot.apihelper.ApiException:
                        bot.send_message(
                            chat_id=message.chat.id,
                            text=%s.format(
                                first_name=message.from_user.first_name,
                                last_name=message.from_user.last_name,
                                username=message.from_user.username,
                                is_bot=message.from_user.is_bot,
                                id=message.from_user.id,
                                message_id=message.message_id
                            )
                        )

            """) % (
                key, repr(key), repr(key), key, repr(value[0]), value[1],
                repr(value[0]), repr(value[0]), repr(value[0]), repr(value[0])
            )

        final_path = os.path.join(PATH, f'{self.__username}')
        path = os.path.join(
            final_path, f'{self.__username}_{self.__token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))


class ReplyMarkupBuilder:
    def __init__(self, token: str, username: str) -> None:
        super().__init__()
        self.__token = token.replace(':', '_')
        self.__username = username
        self.__reply_markup_dictionary = None

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
                        'smart': reply_markup_element['smart'],
                        'buttons': buttons
                    }
                self.__reply_markup_dictionary = final_reply_markup_keyboard
                self.__generate_reply_code()
        except KeyError as k_error:
            k_error = str(k_error)
            print(k_error)

            message = ''
            if k_error == "'buttons'":
                message += ' You have not added buttons to the reply keyboard.'
                return message

    def __generate_reply_code(self):
        smart_dict: dict = {}
        object_text: str = ""

        for key, value in self.__reply_markup_dictionary.items():
            if self.__reply_markup_dictionary[key]['smart'] is True:
                smart_dict[key] = value

        for key in smart_dict.keys():
            if key in self.__reply_markup_dictionary:
                del self.__reply_markup_dictionary[key]

        for key, value in smart_dict.items():
            object_text += textwrap.dedent("""
            def check_similarity_%s(word: Message) -> dict:
                generated_phrases = generate_synonyms(%s.lower())

                word = word.text
                params = {'word': '', 'percent': 0}

                for value in generated_phrases[%s.lower()]:
                    similarity = fuzz.ratio(word, value)
                    if similarity >= params[
                            'percent'] and similarity >= 60:
                        params['word'] = value
                        params['percent'] = similarity
                return True if params['percent'] != 0 else False


            @bot.message_handler(func=check_similarity_%s)
            def handler(message: Message) -> None:
                logger.info(
                    "User -> {user_message} : Bot -> {bot_message}".format(
                        user_message=message.text,
                        bot_message=%s.replace(
                            '\\n', ''
                        )
                    )
                )
                keyboard = ReplyKeyboardMarkup(
                    resize_keyboard=%s,
                    one_time_keyboard=%s,
                    selective=%s,
                    row_width=%s
                )
                some_list = []

                for item in %s:
                    button = KeyboardButton(
                        text=f"{item['response']}",
                        request_contact=item['request_contact'],
                        request_location=item['request_location']
                    )
                    some_list.append(button)
                keyboard.add(*some_list)

                try:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=%s.format(
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            is_bot=message.from_user.is_bot,
                            id=message.from_user.id,
                            message_id=message.message_id
                        ),
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                except telebot.apihelper.ApiException:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=%s.format(
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            is_bot=message.from_user.is_bot,
                            id=message.from_user.id,
                            message_id=message.message_id
                        ),
                        reply_markup=keyboard
                    )

            """ % (
                key, repr(key), repr(key), key,
                repr(value['response_text']),
                value['resize_keyboard'],
                value['one_time_keyboard'],
                value['selective'],
                value['row_width'],
                value['buttons'],
                repr(value['response_text']),
                repr(value['response_text'])
            ))

        if self.__reply_markup_dictionary:
            object_text += textwrap.dedent("""
            reply_markup_dictionary = %s
            @bot.message_handler(
                func=lambda message: message.text in \
reply_markup_dictionary.keys()
            )
            def response_markup(message):
                logger.info(
                    "User -> {user_message} : Bot -> {bot_message}".format(
                        user_message=message.text,
                        bot_message=(reply_markup_dictionary[message.text]['response_text']).replace(
                            '\\n', ''
                        )
                    )
                )
                keyboard = ReplyKeyboardMarkup(
                    resize_keyboard=reply_markup_dictionary[message.text]['resize_keyboard'],
                    one_time_keyboard=reply_markup_dictionary[message.text]['one_time_keyboard'],
                    selective=reply_markup_dictionary[message.text]['selective'],
                    row_width=reply_markup_dictionary[message.text]['row_width']
                )
                some_list = []

                for item in reply_markup_dictionary[message.text]['buttons']:
                    button = KeyboardButton(
                        text=f"{item['response']}",
                        request_contact=item['request_contact'],
                        request_location=item['request_location']
                    )
                    some_list.append(button)
                keyboard.add(*some_list)

                try:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=f"{reply_markup_dictionary[message.text]['response_text']}".format(
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            is_bot=message.from_user.is_bot,
                            id=message.from_user.id,
                            message_id=message.message_id
                        ),
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                except telebot.apihelper.ApiException:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=f"{reply_markup_dictionary[message.text]['response_text']}".format(
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            is_bot=message.from_user.is_bot,
                            id=message.from_user.id,
                            message_id=message.message_id
                        ),
                        reply_markup=keyboard
                    )

            """ % self.__reply_markup_dictionary)

        final_path = os.path.join(PATH, f'{self.__username}')
        path = os.path.join(
            final_path, f'{self.__username}_{self.__token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))


class InlineMarkupBuilder:
    def __init__(self, token: str, username: str) -> None:
        super().__init__()
        self.__token = token.replace(':', '_')
        self.__username = username
        self.__inline_markup_dictionary = None

    def create_option_dict(self, data: dict) -> None:
        try:
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
                        'smart': inline_markup_element['smart'],
                        'buttons': buttons
                    }
                self.__inline_markup_dictionary = final_inline_markup_keyboard
                self.__generate_inline_code()
        except KeyError as k_error:
            k_error = str(k_error)

            message = ''
            if k_error == "'buttons'":
                message += (' You have not added buttons '
                            'to the inline keyboard.')
                return message

    def __generate_inline_code(self):
        smart_dict = {}
        object_text = ""

        for key, value in self.__inline_markup_dictionary.items():
            if self.__inline_markup_dictionary[key]['smart'] is True:
                smart_dict[key] = value

        for key in smart_dict.keys():
            if key in self.__inline_markup_dictionary:
                del self.__inline_markup_dictionary[key]

        for key, value in smart_dict.items():
            object_text += textwrap.dedent("""
            def check_similarity_%s(word: Message) -> dict:
                generated_phrases = generate_synonyms(%s.lower())

                word = word.text
                params = {'word': '', 'percent': 0}

                for value in generated_phrases[%s.lower()]:
                    similarity = fuzz.ratio(word, value)
                    if similarity >= params[
                            'percent'] and similarity >= 60:
                        params['word'] = value
                        params['percent'] = similarity
                return True if params['percent'] != 0 else False


            @bot.message_handler(func=check_similarity_%s)
            def handler(message: Message) -> None:
                logger.info(
                    "User -> {user_message} : Bot -> {bot_message}".format(
                        user_message=message.text,
                        bot_message=%s.replace(
                            '\\n', ''
                        )
                    )
                )
                keyboard = InlineKeyboardMarkup(
                    row_width=%s
                )
                some_list = []

                for item in %s:
                    generator_value = []
                    for value in item.keys():
                        if item[value] is False:
                            item[value] = None
                        generator_value.append(item[value])

                    button = InlineKeyboardButton(*generator_value)
                    some_list.append(button)
                keyboard.add(*some_list)

                try:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=%s.format(
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            is_bot=message.from_user.is_bot,
                            id=message.from_user.id,
                            message_id=message.message_id
                        ),
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                except telebot.apihelper.ApiException:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=%s.format(
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            is_bot=message.from_user.is_bot,
                            id=message.from_user.id,
                            message_id=message.message_id
                        ),
                        reply_markup=keyboard
                    )

            """ % (
                key, repr(key), repr(key), key,
                repr(value['response_text']),
                value['row_width'],
                value['buttons'],
                repr(value['response_text']),
                repr(value['response_text'])
            ))

        if self.__inline_markup_dictionary:
            object_text += textwrap.dedent("""
            inline_markup_dictionary = %s
            @bot.message_handler(
                func=lambda message: message.text in \
inline_markup_dictionary.keys()
            )
            def response_inline(message):
                logger.info(
                    "User -> {user_message} : Bot -> {bot_message}".format(
                        user_message=message.text,
                        bot_message=(inline_markup_dictionary[message.text]['response_text']).replace(
                            '\\n', ''
                        )
                    )
                )
                keyboard = InlineKeyboardMarkup(
                    row_width=inline_markup_dictionary[
                        message.text
                    ]['row_width']
                )
                some_list = []

                for item in inline_markup_dictionary[
                        message.text]['buttons']:
                    generator_value = [
                        item[value] for value in item.keys()
                    ]

                    button = InlineKeyboardButton(*generator_value)
                    some_list.append(button)
                keyboard.add(*some_list)

                try:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=f"{inline_markup_dictionary[message.text]['response_text']}".format(
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            is_bot=message.from_user.is_bot,
                            id=message.from_user.id,
                            message_id=message.message_id
                        ),
                        reply_markup=keyboard,
                        parse_mode='Markdown'
                    )
                except telebot.apihelper.ApiException:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=f"{inline_markup_dictionary[message.text]['response_text']}".format(
                            first_name=message.from_user.first_name,
                            last_name=message.from_user.last_name,
                            username=message.from_user.username,
                            is_bot=message.from_user.is_bot,
                            id=message.from_user.id,
                            message_id=message.message_id
                        ),
                        reply_markup=keyboard
                    )

            """ % self.__inline_markup_dictionary)

        final_path = os.path.join(PATH, f'{self.__username}')
        path = os.path.join(
            final_path, f'{self.__username}_{self.__token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))


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
                for callback_element in data['callbacks']:
                    for value_1 in data['text']:
                        if callback_element['react_text'] == \
                                value_1['react_text']:
                            final_callback_query[
                                callback_element['callback']
                            ] = value_1
                self.__callback_dictionary = final_callback_query
                self.__generate_callback_code()
        except KeyError as k_error:
            print(k_error)

    def __generate_callback_code(self):
        object_text = ''
        for key, value in self.__callback_dictionary.items():
            object_text += textwrap.dedent(f"""
            @bot.callback_query_handler(
                func=lambda call: call.data == '%s' % '{key}')
            def get_callback(call):
                try:
                    bot.send_message(
                        chat_id=call.from_user.id,
                        text={repr(value['response_text'])}.format(
                            first_name=call.from_user.first_name,
                            last_name=call.from_user.last_name,
                            username=call.from_user.username,
                            is_bot=call.from_user.is_bot,
                            id=call.from_user.id
                        ),
                        parse_mode='Markdown'
                    )
                except telebot.apihelper.ApiException:
                    bot.send_message(
                        chat_id=call.from_user.id,
                        text={repr(value['response_text'])}.format(
                            first_name=call.from_user.first_name,
                            last_name=call.from_user.last_name,
                            username=call.from_user.username,
                            is_bot=call.from_user.is_bot,
                            id=call.from_user.id
                        )
                    )
                except Exception as error:
                    print(error)

            """)

        final_path = os.path.join(PATH, f'{self.__username}')
        path = os.path.join(
            final_path, f'{self.__username}_{self.__token}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))
