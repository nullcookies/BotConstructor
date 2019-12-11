from django.conf import settings
from abc import ABC, abstractmethod, abstractproperty
import textwrap
import os


PATH = os.path.join(settings.BASE_DIR, 'BotConstructor', 'media', 'ScriptsBots')


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
        path = os.path.join(PATH, f'{user_username}_test_bot.py')
        with open(path, 'w', encoding='utf-8') as file:
            file.write(textwrap.dedent(init_object))

    def text_response(self, text_dictionary) -> None:
        object_text = """
        text_dictionary_messages = %s
        @bot.message_handler(func=lambda message: message.text in text_dictionary_messages.keys())
        def response_message(message):
            print(text_dictionary_messages[message.text])
            bot.send_message(chat_id=message.chat.id, text=f'{text_dictionary_messages[message.text]}')

        """ % text_dictionary

        with open('test_bot.py', 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))

    def reply_markup_response(self, reply_markup_dictionary):
        object_text = """
        reply_markup_dictionary = %s
        @bot.message_handler(func=lambda message: message.text in reply_markup_dictionary.keys())
        def response_markup(message):
            keybord = ReplyKeyboardMarkup(
            resize_keyboard=reply_markup_dictionary[message.text]['resize_keyboard'], one_time_keyboard=reply_markup_dictionary[message.text]['one_time_keyboard'], selective=reply_markup_dictionary[message.text]['selective'], row_width=reply_markup_dictionary[message.text]['row_width'])

            for item in reply_markup_dictionary[message.text]['buttons']:
                button = KeyboardButton(text=f"{item['response']}", request_contact=item['request_contact'], request_location=item['request_location'])
                keybord.add(button)

            bot.send_message(chat_id=message.chat.id, text=f"{reply_markup_dictionary[message.text]['response_text']}", reply_markup=keybord)

        """ % reply_markup_dictionary

        path = os.path.join(PATH, f'{self.user_username}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))

    def polling_bot(self):
        polling_object = f"""
        bot.polling(none_stop=True)
        """

        path = os.path.join(PATH, f'{self.user_username}_test_bot.py')
        with open(path, 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(polling_object))


# some_object = TextBuilder('772271583:AAHh-K3sPqcTPTkoM9Ah_S7jdhOIdL_LmpM')
# some_object.text_response(text_dictionary={'dasdasd': 'asdasdasd'})
# some_object.polling_bot()
