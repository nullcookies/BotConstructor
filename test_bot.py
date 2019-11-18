import telebot

bot = telebot.TeleBot(token='952347487:AAFYaR_Dca1phyvrX4OO1xZyTBPp5O8-xI4')


@bot.message_handler(func=lambda message: message.text == 'hi')
def hello(message):
    bot.send_message(chat_id=message.chat.id, text='hello')


@bot.message_handler(func=lambda message: message.text == 'thing')
def some(message):
    bot.send_message(chat_id=message.chat.id, text='some')


bot.polling(none_stop=True)
