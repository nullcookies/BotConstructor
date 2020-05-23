import requests
import os
import json
import string
import re

from pprint import pprint
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sys import platform


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AutoDeploy:
    def __init__(self, file_title: str):
        self.path = os.path.join(BASE_DIR, 'BotConstructor', 'media',
                                 'ScriptsBots', f"{file_title.split('_')[0]}",
                                 file_title.replace(':', '_'))
        self.file_title = file_title.replace(':', '_')

        # ! User credencials
        self.TOKEN = '54be38d4e853d62835b2c970d6b6fc23a653b901'
        self.HEADERS = {
            'Authorization': f'Token {self.TOKEN}'
        }
        self.USERNAME = 'AlexanderIvanov20'
        self.BASE_URL = 'https://www.pythonanywhere.com'

        # ? Open and write content of a file
        self.DATA = open(self.path, 'r', encoding='utf-8').read()
        self.PATH = f"/home/{self.USERNAME}/{file_title.replace(':', '_')}"
        self.FILES = {
            'content': self.DATA
        }

        # ? Params for create console
        self.PARAMS = {
            'executable': 'bash',
            'arguments': '',
            'working_directory': f'/home/{self.USERNAME}/'
        }

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
        options = Options()
        options.headless = True

        if platform == 'linux' or platform == 'linux2':
            executable_path = '/usr/lib/chromium-browser/chromedriver'
        elif platform == "win32":
            executable_path = os.path.join(
                BASE_DIR, 'chromedriver.exe'
            )

        # ? Open driver
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

    def send_input(self, console_id: int):
        # ! Send command to console
        send_console_response = requests.post(
            f'{self.BASE_URL}/api/v0/user/{self.USERNAME}'
            f'/consoles/{console_id}/send_input/',
            headers=self.HEADERS, json={
                'input': "workon venv\npython3 "
                         f"{self.file_title.replace(':', '_')}\n"
            }
        )

        # ! Check in success
        if send_console_response.status_code in (200, 201):
            pprint(send_console_response.json())
        else:
            print(send_console_response.status_code)

    def stop_bot(self, console_id: int) -> None:
        response = requests.delete(
            f'{self.BASE_URL}/api/v0/user/{self.USERNAME}/'
            f'consoles/{console_id}/',
            headers=self.HEADERS
        )

    def run_bot(self, path) -> None:
        console_id = self.create_console()

        with open(path, 'r+', encoding='utf-8') as file:
            object_config = json.load(file)
            object_config['console_id'] = console_id
            file.seek(0)
            json.dump(object_config, file,
                      indent=4, ensure_ascii=False)

        self.open_console()
        self.send_input(console_id)

    def _write_to_log_file(self, request, token: str,
                           data: dict, username: str, console_id: int) -> None:
        path = os.path.join(
            BASE_DIR, 'BotConstructor', 'media',
            'ScriptsBots', username,
            "{}_{}_output.log".format(username, token.replace(':', '_'))
        )
        response = requests.get(
            self.BASE_URL +
            '/api/v0/user/{username}/consoles/{id}/get_latest_output/'.format(
                username=self.USERNAME,
                id=str(console_id)
            ),
            headers={
                'Authorization': 'Token {token}'.format(token=self.TOKEN)
            }
        )
        if response.status_code == 200:
            output = response.json()["output"]

            ansi_escape = re.compile(
                r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", re.VERBOSE)
            result = ansi_escape.sub('', output)

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
    print(data)

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
