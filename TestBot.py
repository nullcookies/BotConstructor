import telebot
# from flask import Flask, request

TOKEN = '944380578:AAEFvaqShiw164lLumAu2wI6w2ZnzSAJ7lM'
bot = telebot.TeleBot(TOKEN)


# bot.remove_webhook()
# bot.set_webhook(url=url)
# app = Flask(__name__)
# # sslify = SSLify(app)


# @app.route(f'/{secret}', methods=['POST'])
# def webhook():
#     update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
#     bot.process_new_updates([update.message])
#     return 'Ok', 200


@bot.message_handler(commands=['start'])
def greeting(message):
    reply_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                     one_time_keyboard=True,
                                                     row_width=1)
    button = telebot.types.KeyboardButton(text='Hello btn')
    reply_markup.add(button)
    bot.send_message(message.chat.id, 'Hello, I\'m bot', reply_markup=reply_markup)


@bot.message_handler(func=lambda message: True)
def test_function(message):
    keyboard = telebot.types.ReplyKeyboardRemove()
    bot.send_message(chat_id=message.chat.id,
                     text='Delete prev markup', reply_markup=keyboard)


bot.polling()
