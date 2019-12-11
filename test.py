# string = 'Hello '
# print(f'sdsd{string.strip()}ada')
# import telebot
# from telebot.types import *



# some = {
#     'react': {
#         'resize_keyboard': True,
#         'one_time_keyboard': True,
#         'selective': False,
#         'response_text': 'Hello',
#         'buttons': [
#             {
#                 'response': 'some_text',
#                 'request_contact': True,
#                 'request_location': False
#             }
#         ]
#     }
# }


# @bot.message_handler(func=lambda message: message.text in some.keys())
# def main(message):
#     keybord = ReplyKeyboardMarkup(
#         resize_keyboard=some[message.text]['resize_keyboard'], one_time_keyboard=some[message.text]['one_time_keyboard'], selective=some[message.text]['selective'], row_width=1)

#     for item in some[message.text]['buttons']:
#         button = KeyboardButton(
#             text=f"{item['response']}", request_contact=item['request_contact'], request_location=item['request_location'])
#         keybord.add(button)

#     bot.send_message(chat_id=message.chat.id,
#                      text=f"{some[message.text]['response_text']}", reply_markup=keybord)


# bot.polling()


import os


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# path = os.path.join(BASE_DIR, 'BotConstructor', 'media')
# print(path)


test = 'C:\\Users\\user\\Documents\\BotConstructor\\BotConstructor\\media\\ScriptsBots\\AlexanderIvanov'
os.makedirs(test)