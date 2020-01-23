import telebot
from telebot.types import *

bot = telebot.TeleBot(token='фывфыв')


text_dictionary_messages = {'фывфыв': 'ыыс'}
@bot.message_handler(func=lambda message: message.text in text_dictionary_messages.keys())
def response_message(message):
    print(text_dictionary_messages[message.text])
    bot.send_message(chat_id=message.chat.id, text=f'{text_dictionary_messages[message.text]}')


reply_markup_dictionary = {'ываыва': {'resize_keyboard': True, 'one_time_keyboard': True, 'selective': False, 'row_width': 1, 'response_text': 'фыф', 'buttons': [{'response': 'ываыв', 'request_contact': True, 'request_location': False}]}}
@bot.message_handler(func=lambda message: message.text in reply_markup_dictionary.keys())
def response_markup(message):
    keybord = ReplyKeyboardMarkup(
    resize_keyboard=reply_markup_dictionary[message.text]['resize_keyboard'], one_time_keyboard=reply_markup_dictionary[message.text]['one_time_keyboard'], selective=reply_markup_dictionary[message.text]['selective'], row_width=reply_markup_dictionary[message.text]['row_width'])

    for item in reply_markup_dictionary[message.text]['buttons']:
        button = KeyboardButton(text=f"{item['response']}", request_contact=item['request_contact'], request_location=item['request_location'])
        keybord.add(button)

    bot.send_message(chat_id=message.chat.id, text=f"{reply_markup_dictionary[message.text]['response_text']}", reply_markup=keybord)


bot.polling(none_stop=True)
