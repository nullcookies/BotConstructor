import os
import json
import random

from telebot.types import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA = {}


def send_message(start_user: int, username_user: str, password_user: str,
                 message: str) -> None:
    start_user = int(start_user)

    driver_path = os.path.join(BASE_PATH, 'chromedriver.exe')
    print(driver_path)

    driver = webdriver.Chrome(driver_path)
    driver.maximize_window()
    driver.get(
        'https://www.linkedin.com/login?fromSignIn=true&trk='
        'guest_homepage-basic_nav-header-signin'
    )

    username = driver.find_element_by_xpath('//*[@id="username"]')
    password = driver.find_element_by_xpath('//*[@id="password"]')

    username.send_keys(username_user)
    password.send_keys(password_user)
    driver.find_element_by_xpath(
        '//*[@id="app__container"]/main/div/form/div[3]/button').submit()
    sleep(1)

    driver.get(
        'https://www.linkedin.com/mynetwork/invite-connect/connections/'
    )

    count_contacts = int(driver.find_element_by_xpath(
        '//*[@class="mn-connections mb4 artdeco-card ember-view"]/header/h1'
    ).text.split(' ')[0])

    for item in range(0, count_contacts//40 + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        sleep(1)

    ul_a = driver.find_element_by_xpath(
        '//*[@class="mn-connections mb4 artdeco-card ember-view"]/ul'
    )
    lis_some = ul_a.find_elements_by_css_selector('.list-style-none')
    sleep(3)
    driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
    sleep(3)

    iterator = start_user
    for li_c in lis_some:
        li_c.find_element_by_xpath(
            '/html/body/div[5]/div[4]/div[3]/div/div/div/div/div/div/div/div'
            f'/section/ul/li[{iterator}]/div/div[2]/div/button'
        ).click()
        sleep(1)
        li_c.find_element_by_xpath(
            '//*[@class="msg-form__message-texteditor relative flex-grow-1 '
            'display-flex ember-view"]/div[1]'
        ).send_keys(message)
        sleep(1)
        li_c.find_element_by_xpath(
            '//*[@class="msg-form__right-actions display-flex '
            'align-items-center"]//*[@class="ember-view"]/button'
        ).click()
        sleep(1)
        try:
            sleep(1)
            li_c.find_element_by_xpath(
                '//*[@class="artdeco-modal artdeco-modal--layer-default '
                'msg-modal-discard-message"]//*[@class="artdeco-button '
                'artdeco-button--2 artdeco-button--primary ember-view"]'
            ).click()
            sleep(1)
        except Exception:
            pass
        li_c.find_element_by_xpath(
            '//*[@class="msg-overlay-bubble-header__control js-msg-close '
            'artdeco-button artdeco-button--circle artdeco-button--inverse '
            'artdeco-button--1 artdeco-button--tertiary ember-view"]'
        ).click()
        iterator += 1
    driver.close()


@bot.message_handler(commands=['start'])
def on_start(message: Message) -> None:
    bot.send_message(
        chat_id=message.from_user.id,
        text='Hello. Here you can mail to your friends on Linked In.\n\n'
             'To start, mailing enter your username and password in '
             '`{username} {password}` format',
        parse_mode='Markdown'
    )


@bot.message_handler(
    func=lambda message: '{' in message.text and '}' in message.text
)
def get_credentials(message: Message) -> None:
    credenrials = message.text.replace('{', '')
    credenrials = credenrials.replace('}', '').split(' ')

    with open(os.path.join(
        BASE_PATH, f'{message.from_user.id}_creds.json'
    ), 'w', encoding='utf-8') as file:
        json.dump({
            'email': credenrials[0],
            'password': credenrials[1]
        }, file, indent=4)

    msg = bot.send_message(
        chat_id=message.from_user.id,
        text='Now, enter a message that you want to send out'
    )
    bot.register_next_step_handler(msg, get_message)


def get_message(message: Message):
    user_message = message.text

    with open(os.path.join(
        BASE_PATH, f'{message.from_user.id}_creds.json'
    ), 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(data)

    try:
        send_message(start_user=1, username_user=data['email'],
                     password_user=data['password'], message=user_message)
    except Exception as error:
        print(error)
        bot.send_message(chat_id=message.from_user.id,
                         text='You have already stoped the mailing')

    os.remove(os.path.join(BASE_PATH, f'{message.from_user.id}_creds.json'))


bot.polling(none_stop=True)
