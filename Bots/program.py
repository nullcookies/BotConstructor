from abc import ABC, abstractmethod, abstractproperty
import textwrap


class Builder(ABC):
    @abstractmethod
    def text_response(self) -> None:
        pass


class TextBuilder(Builder):
    def __init__(self, token):
        init_object = f"""\
        import telebot

        bot = telebot.TeleBot(token='{token}')

        """
        with open('test_bot.py', 'w', encoding='utf-8') as file:
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

    def polling_bot(self):
        polling_object = f"""
        bot.polling(none_stop=True)
        """

        with open('test_bot.py', 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(polling_object))


some_object = TextBuilder('772271583:AAHh-K3sPqcTPTkoM9Ah_S7jdhOIdL_LmpM')
some_object.text_response(text_dictionary={'dasdasd': 'asdasdasd'})
some_object.polling_bot()
