from GoogleNews import GoogleNews


google_news = GoogleNews()


@bot.message_handler(commands=['start'])
def on_start(message: Message) -> None:
    bot.send_message(
        chat_id=message.from_user.id,
        text='Здравствуйте.\n\nВас привествует Telegram бот.\n'
             'Здесь Вы можете узнать нововости по интересующей Вам теме.\n\n'
             'Нажмите на /news и следуйте инструкциям'
    )


@bot.message_handler(commands=['news'])
def on_news(message: Message) -> None:
    message = bot.send_message(
        chat_id=message.chat.id,
        text='Введите текст, что бы найти новости '
    )
    bot.register_next_step_handler(
        message=message,
        callback=answer_news
    )


def answer_news(message: Message):
    google_news.search(message.text.strip())
    google_news.getpage(1)
    results = google_news.result()
    google_news.clear()

    print(results)

    if results != []:
        for item in results:
            bot.send_message(
                chat_id=message.chat.id,
                text=f"Название: {item['title']}\n"
                f"Источник: {item['media']}\n"
                f"Подробнее: {item['desc']}\n"
                f"Ссылка: {item['link']}\n"
                f"Дата: {item['date']}"
            )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='Новостей на это ключевое слово не найдено.\n\n'
                 'Попробуйте еще раз /news'
        )


@bot.message_handler(func=lambda message: True)
def exception(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Я не могу обработать введенный Вами текст...\n\n'
             'Список поддерживаемых комманд: /news'
    )


bot.polling(none_stop=True)
