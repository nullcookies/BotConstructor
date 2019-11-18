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

    def text_response(self, response_text, react_text) -> None:
        object_text = f"""
        @bot.message_handler(func=lambda message: message.text == '{react_text}')
        def {response_text}(message):
            bot.send_message(chat_id=message.chat.id, text='{response_text}')

        """

        with open('test_bot.py', 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(object_text))

    def polling_bot(self):
        polling_object = f"""
        bot.polling(none_stop=True)
        """

        with open('test_bot.py', 'a', encoding='utf-8') as file:
            file.write(textwrap.dedent(polling_object))


text_builder = TextBuilder('952347487:AAFYaR_Dca1phyvrX4OO1xZyTBPp5O8-xI4')
text_builder.text_response('hello', 'hi')
text_builder.text_response('some', 'thing')
text_builder.polling_bot()
