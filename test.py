# string = 'Hello '
# print(f'sdsd{string.strip()}ada')
# import telebot

# import telebot
# from telebot.types import *

# bot = telebot.TeleBot(token='944380578:AAEFvaqShiw164lLumAu2wI6w2ZnzSAJ7lM')

# inline_markup_dictionary = {
#     'Hello': {
#         'buttons': [
#             {
#                 'text': 'Some',
#                 'url': 'https://google.com',
#                 'callback': '',
#                 'switch_inline': '',
#                 'switch_inline_current': '',
#             },
#             {
#                 'text': 'some',
#                 'url': '',
#                 'callback': '',
#                 'switch_inline': 'asdasd',
#                 'switch_inline_current': '',
#             },
#             {
#                 "text": "asdsad",
#                 "url": "",
#                 "callback": "asdada",
#                 "switch_inline": "",
#                 "switch_inline_current": ""
#             }
#         ],
#         'response_text': 'A-ha',
#         'row_width': 2
#     }
# }
# @bot.message_handler(func=lambda message: message.text in \
# inline_markup_dictionary.keys())
# def response_inline(message):
#     keyboard = InlineKeyboardMarkup(row_width=inline_markup_dictionary[
#         message.text
#     ]['row_width'])
#     some_list = []

#     for item in inline_markup_dictionary[message.text]['buttons']:
#         generator_value = [
#             item[value] for value in item.keys()
#         ]

#         button = InlineKeyboardButton(*generator_value)
#         some_list.append(button)
#     keyboard.add(*some_list)

#     bot.send_message(chat_id=message.chat.id,
#                      text=f"{inline_markup_dictionary[message.text]['response_text']}",
#                      reply_markup=keyboard)


# bot.polling()


# import os


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# path = os.path.join(BASE_DIR, 'BotConstructor', 'media')
# print(path)


# test = 'C:\\Users\\user\\Documents\\BotConstructor\\BotConstructor
# \\media\\ScriptsBots\\AlexanderIvanov'
# os.makedirs(test)


# s = 'asd_a_w_sds'
# s = s[:s.rfind('_')]
# print(s)

# s = 'asdsdasd\nsdfsdf'
# print(s)
item = {
    "text": "sdfsdf",
    "url": "",
    "callback": "sdfsdf",
    "switch_inline": "",
    "switch_inline_current": ""
}
generator_value = [value for value in item.keys() if item[value] != ""]
print(generator_value)
