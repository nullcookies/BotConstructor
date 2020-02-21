# string = 'Hello '
# print(f'sdsd{string.strip()}ada')
# import telebot

# import telebot
# from telebot.types import *

# bot = telebot.TeleBot(token='944380578:AAEFvaqShiw164lLumAu2wI6w2ZnzSAJ7lM')
# ReplyKeyboardRemove

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

# d = {
#     'asdasd': ['sdsdf', True],
#     'sd': ['asd', False]
# }
# s = {}

# for key, value in d.items():
#     if d[key][1] is True:
#         s[key] = value

# for i in s.keys():
#     if i in d.keys():
#         del d[i]
# print(d, s)


import requests

url = 'https://www.pythonanywhere.com/login/'


session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.116 Safari/537.36'
})


response = session.get(url)

session.headers.update({
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www.pythonanywhere.com',
    'Referer': 'https://www.pythonanywhere.com/login/',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
})

some = session.cookies.get_dict()
data = {
    'csrfmiddlewaretoken': some['csrftoken'],
    'auth-username': 'AlexanderIvanov20',
    'auth-password': 'QBmhyq.c_Khi62%',
    'login_view-current_step': 'auth'
}
resp = session.post(url, data=data)
print(resp.status_code)

session.get(
    'https://www.pythonanywhere.com/user/AlexanderIvanov20/consoles/14862405/')
