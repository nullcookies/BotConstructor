import requests
import os
import json
import string
import re

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sys import platform
from django.conf import settings


class AutoDeploy:
    def __init__(self, file_title: str):
        self.path = os.path.join(settings.BASE_DIR, 'BotConstructor', 'media',
                                 'ScriptsBots', f"{file_title.split('_')[0]}",
                                 file_title.replace(':', '_'))
        self.file_title = file_title.replace(':', '_')

        self.TOKEN = '54be38d4e853d62835b2c970d6b6fc23a653b901'
        self.HEADERS = {'Authorization': f'Token {self.TOKEN}'}
        self.USERNAME = 'AlexanderIvanov20'
        self.BASE_URL = 'https://www.pythonanywhere.com'

        self.PATH = f"/home/{self.USERNAME}/{self.file_title}"

        self.PARAMS = {
            'executable': 'bash',
            'arguments': '',
            'working_directory': f'/home/{self.USERNAME}/'
        }

    # Do request for upload file
    def upload_file(self) -> None:
        self.DATA = open(self.path, 'r', encoding='utf-8').read()
        self.FILES = {'content': self.DATA}
        response = requests.post(
            f'{self.BASE_URL}/api/v0/user/{self.USERNAME}'
            f'/files/path{self.PATH}',
            headers=self.HEADERS, files=self.FILES
        )

    # Delete file. Use this method if bot will delete.
    def delete_file(self) -> None:
        response = requests.delete(
            f'{self.BASE_URL}/api/v0/user/{self.USERNAME}'
            f'/files/path{self.PATH}',
            headers=self.HEADERS
        )

    # Create a console and get console id
    def create_console(self):
        console_response = requests.post(
            f'{self.BASE_URL}/api/v0/user/{self.USERNAME}/consoles/',
            headers=self.HEADERS, data=self.PARAMS
        )
        console_id = console_response.json()['id']
        return console_id

    # Open last console to activate it
    def open_console(self):
        options = Options()
        options.headless = True

        if platform == 'linux' or platform == 'linux2':
            executable_path = '/usr/lib/chromium-browser/chromedriver'
        elif platform == "win32":
            executable_path = os.path.join(
                settings.BASE_DIR, 'chromedriver.exe'
            )
        driver = webdriver.Chrome(
            executable_path=executable_path,
            chrome_options=options
        )
        driver.get(
            f'{self.BASE_URL}/user/{self.USERNAME}/consoles/#'
        )
        username = driver.find_element_by_xpath('//*[@id="id_auth-username"]')
        password = driver.find_element_by_xpath('//*[@id="id_auth-password"]')
        button = driver.find_element_by_xpath('//*[@id="id_next"]')
        username.send_keys('AlexanderIvanov20')
        password.send_keys('QBmhyq.c_Khi62%')
        button.click()
        sleep(1)
        driver.get(
            f'{self.BASE_URL}/user/AlexanderIvanov20/consoles/#')
        driver.find_element_by_xpath(
            '//*[@id="id_consoles"]/div/div[2]/table/tbody'
        ).find_elements_by_tag_name('tr')[-1].find_elements_by_tag_name(
            'td'
        )[0].find_element_by_xpath('a').click()
        sleep(2.5)
        driver.close()

    #  Send command to console
    def send_input(self, console_id: int):
        send_console_response = requests.post(
            f'{self.BASE_URL}/api/v0/user/{self.USERNAME}'
            f'/consoles/{console_id}/send_input/',
            headers=self.HEADERS, json={
                'input': "workon venv\npython3 "
                         f"{self.file_title.replace(':', '_')}\n"
            }
        )
        if send_console_response.status_code in (200, 201):
            print(send_console_response.json())
        else:
            print(send_console_response.status_code)

    def stop_bot(self, console_id: int) -> None:
        response = requests.delete(
            f'{self.BASE_URL}/api/v0/user/{self.USERNAME}/'
            f'consoles/{console_id}/',
            headers=self.HEADERS
        )

    def run_bot(self, path) -> None:
        self.upload_file()
        console_id = self.create_console()

        with open(path, 'r+', encoding='utf-8') as file:
            object_config = json.load(file)
            object_config['console_id'] = console_id
            file.seek(0)
            json.dump(object_config, file,
                      indent=4, ensure_ascii=False)

        self.open_console()
        self.send_input(console_id)

    # Write logs in file so that the user sees, what
    # id going on with his/her bot
    def _write_to_log_file(self, request, token: str, console_id: int) -> None:
        path = os.path.join(
            settings.BASE_DIR, 'BotConstructor', 'media',
            'ScriptsBots', request.user.username,
            "{}_{}_output.log".format(
                request.user.username, token.replace(':', '_'))
        )
        response = requests.get(
            self.BASE_URL +
            '/api/v0/user/{username}/consoles/{id}/get_latest_output/'.format(
                username=self.USERNAME,
                id=str(console_id)
            ),
            headers=self.HEADERS
        )
        print(response)
        if response.status_code == 200:
            output = response.json()["output"]

            ansi_escape = re.compile(
                r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", re.VERBOSE)
            result = ansi_escape.sub('', output).replace('\r', '')

            printable = set(string.printable)
            new_output = ''.join(filter(lambda x: x in printable, result))

            with open(path, 'w') as file:
                file.write("{output}\n".format(output=new_output.strip()))
        else:
            print('Got unexpected status code {}: {!r}'.format(
                response.status_code, response.content))


def get_status_of_console(console_id: int) -> bool:
    TOKEN = '54be38d4e853d62835b2c970d6b6fc23a653b901'
    HEADERS = {
        'Authorization': f'Token {TOKEN}'
    }
    USERNAME = 'AlexanderIvanov20'
    BASE_URL = 'https://www.pythonanywhere.com'

    current_console_url = (
        f'{BASE_URL}/api/v0/user/'
        f'{USERNAME}/consoles/{console_id}/'
    )
    status_id_console = requests.get(
        current_console_url, headers=HEADERS)
    data = status_id_console.json()

    if 'detail' in data.keys():
        return False
    else:
        return True


if __name__ == '__main__':
    deploy = AutoDeploy(
        "AlexanderIvanov_"
        "1023044822_AAFFTiQYlALBh7kydHwpSGtTT_q9xV9Vens_test_bot.py"
    )
    deploy._write_to_log_file()
