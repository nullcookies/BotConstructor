import telebot
from telebot.types import *

bot = telebot.TeleBot(token='1024355119:AAEQqdnfPe8TXwz0GSfk64QHKpwto9mL3nk')

text_dictionary_messages = {}


@bot.message_handler(func=lambda message: message.text in text_dictionary_messages.keys())
def response_message(message):
    print(text_dictionary_messages[message.text])
    bot.send_message(chat_id=message.chat.id,
                     text=f'{text_dictionary_messages[message.text][0]}',
                     reply_markup=ReplyKeyboardRemove())


@bot.message_handler(
    func=lambda message: message.text == 'sdfsdfsdf'
)
def response_message_remove(message):
    bot.send_message(chat_id=message.chat.id,
                     text='sdfsdfs',
                     reply_markup=ReplyKeyboardRemove())


bot.polling(none_stop=True)



bot.polling(none_stop=True)
