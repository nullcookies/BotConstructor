import requests
import os

from pprint import pprint
from time import sleep
from selenium import webdriver


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AutoDeploy:
    def __init__(self, file_title: str):
        self.path = os.path.join(BASE_DIR, 'BotConstructor', 'media',
                                 'ScriptsBots', f"{file_title.split('_')[0]}",
                                 file_title)
        self.file_title = file_title

        # ! User credencials
        self.TOKEN = '54be38d4e853d62835b2c970d6b6fc23a653b901'
        self.HEADERS = {
            'Authorization': f'Token {self.TOKEN}'
        }
        self.USERNAME = 'AlexanderIvanov20'
        self.BASE_URL = 'https://www.pythonanywhere.com'

        # ? Open and write content of a file
        self.DATA = open(self.path, 'r', encoding='utf-8').read()
        self.PATH = f'/home/{self.USERNAME}/{file_title}'
        self.FILES = {
            'content': self.DATA
        }

        # ? Params for create console
        self.PARAMS = {
            'executable': 'bash',
            'arguments': '',
            'working_directory': f'/home/{self.USERNAME}/'
        }

        # Call the functions
        self.upload_file()
        self.CONSOLE_ID = self.create_console()
        self.open_console()
        self.send_input()

    def upload_file(self):
        # ! Do request for upload file
        response = requests.post(
            f'{self.BASE_URL}/api/v0/user/{self.USERNAME}'
            f'/files/path{self.PATH}',
            headers=self.HEADERS, files=self.FILES
        )

    def create_console(self):
        # ! Create a console
        console_response = requests.post(
            f'{self.BASE_URL}/api/v0/user/{self.USERNAME}/consoles/',
            headers=self.HEADERS, data=self.PARAMS
        )

        # ! Get console id
        console_id = console_response.json()['id']
        return console_id

    def open_console(self):
        # ? Open driver
        driver = webdriver.Chrome(
            executable_path=os.path.join(BASE_DIR, 'chromedriver.exe')
        )
        driver.get(
            f'{self.BASE_URL}/user/{self.USERNAME}/consoles/#'
        )
        username = driver.find_element_by_xpath('//*[@id="id_auth-username"]')
        password = driver.find_element_by_xpath('//*[@id="id_auth-password"]')
        button = driver.find_element_by_xpath('//*[@id="id_next"]')

        # ? Authorization
        username.send_keys('AlexanderIvanov20')
        password.send_keys('QBmhyq.c_Khi62%')
        button.click()
        sleep(2)

        # ! Open last console
        driver.get(
            f'{self.BASE_URL}/user/AlexanderIvanov20/consoles/#')
        driver.find_element_by_xpath(
            '//*[@id="id_consoles"]/div/div[2]/table/tbody'
        ).find_elements_by_tag_name('tr')[-1].find_elements_by_tag_name(
            'td'
        )[0].find_element_by_xpath('a').click()
        sleep(5)
        driver.close()

    def send_input(self):
        # ! Send command to console
        send_console_response = requests.post(
            f'{self.BASE_URL}/api/v0/user/{self.USERNAME}'
            f'/consoles/{self.CONSOLE_ID}/send_input/',
            headers=self.HEADERS, json={
                'input': f'workon venv\npython3 {self.file_title}\n'}
        )

        # ! Check in success
        if send_console_response.status_code in (200, 201):
            pprint(send_console_response.json())
        else:
            print(send_console_response.status_code)


# parser = AutoDeploy(file_title='AlexanderIvanov_test_bot.py')
