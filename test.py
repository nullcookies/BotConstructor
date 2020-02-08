# string = 'Hello '
# print(f'sdsd{string.strip()}ada')
# import telebot

# import telebot
# from telebot.types import *

# bot = telebot.TeleBot(token='944380578:AAEFvaqShiw164lLumAu2wI6w2ZnzSAJ7lM')


# @bot.inline_handler(func=lambda query: True)
# def query_text(query: InlineQuery) -> None:
#     try:
#         r = InlineQueryResultArticle(
#             id='1',
#             title='Something',
#             input_message_content=InputTextMessageContent(
#                 'hello'
#             ),
#             url='https://google.com',
#             description='Somewhere'
#         )
#         bot.answer_inline_query(query.id, [r])
#     except Exception as error:
#         print(error)


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
# item = {
#     "text": "sdfsdf",
#     "url": "",
#     "callback": "sdfsdf",
#     "switch_inline": "",
#     "switch_inline_current": ""
# }
# generator_value = [value for value in item.keys() if item[value] != ""]
# print(generator_value)
