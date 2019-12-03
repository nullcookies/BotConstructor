import telebot

bot = telebot.TeleBot(token='772271583:AAHh-K3sPqcTPTkoM9Ah_S7jdhOIdL_LmpM')


text_dictionary_messages = {'dasdasd': 'asdasdasd'}
@bot.message_handler(func=lambda message: message.text in text_dictionary_messages.keys())
def response_message(message):
    print(text_dictionary_messages[message.text])
    bot.send_message(chat_id=message.chat.id, text=f'{text_dictionary_messages[message.text]}')


bot.polling(none_stop=True)
