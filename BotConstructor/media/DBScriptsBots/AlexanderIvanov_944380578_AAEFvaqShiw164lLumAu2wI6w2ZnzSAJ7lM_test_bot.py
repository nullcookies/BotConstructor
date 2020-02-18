import telebot
from telebot.types import *

bot = telebot.TeleBot(token='944380578:AAEFvaqShiw164lLumAu2wI6w2ZnzSAJ7lM')

text_dictionary_messages = {}


@bot.message_handler(func=lambda message: message.text in text_dictionary_messages.keys())
def response_message(message):
    print(text_dictionary_messages[message.text])
    bot.send_message(chat_id=message.chat.id,
                     text=f'{text_dictionary_messages[message.text][0]}',
                     reply_markup=ReplyKeyboardRemove())


@bot.message_handler(
    func=lambda message: message.text == 'Hello'
)
def response_message_remove(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Hi',
                     reply_markup=ReplyKeyboardRemove())


bot.polling(none_stop=True)



bot.polling(none_stop=True)
