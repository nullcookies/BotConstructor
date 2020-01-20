import requests

from pprint import pprint
from time import sleep
from selenium import webdriver

# ! User credencials
TOKEN = '54be38d4e853d62835b2c970d6b6fc23a653b901'
HEADERS = {
    'Authorization': f'Token {TOKEN}'
}
USERNAME = 'AlexanderIvanov20'
BASE_URL = 'https://www.pythonanywhere.com'

# ? Open and write content of a file
DATA = open(r'C:\Users\user\Documents\BotConstructor\TestBot.py', 'r').read()
PATH = f'/home/{USERNAME}/Bot.py'
FILES = {
    'content': DATA
}

# ? Params for create console
PARAMS = {
    'executable': 'bash',
    'arguments': '',
    'working_directory': f'/home/{USERNAME}/'
}

# ! Do request for upload file
response = requests.post(
    f'{BASE_URL}/api/v0/user/{USERNAME}/files/path{PATH}',
    headers=HEADERS, files=FILES
)

# ! Create a console
console_response = requests.post(
    f'{BASE_URL}/api/v0/user/{USERNAME}/consoles/',
    headers=HEADERS, data=PARAMS
)

# ! Get console id
console_id = console_response.json()['id']
print(console_id)

# ? Open driver
driver = webdriver.Chrome(
    executable_path=r'C:\Users\user\Desktop\Something\chromedriver.exe'
)
driver.get('https://www.pythonanywhere.com/user/AlexanderIvanov20/consoles/#')
username = driver.find_element_by_xpath('//*[@id="id_auth-username"]')
password = driver.find_element_by_xpath('//*[@id="id_auth-password"]')
button = driver.find_element_by_xpath('//*[@id="id_next"]')

# ? Authorization
username.send_keys('AlexanderIvanov20')
password.send_keys('QBmhyq.c_Khi62%')
button.click()
sleep(2)

# ! Open last console
driver.get('https://www.pythonanywhere.com/user/AlexanderIvanov20/consoles/#')
driver.find_element_by_xpath(
    '//*[@id="id_consoles"]/div/div[2]/table/tbody'
).find_elements_by_tag_name('tr')[-1].find_elements_by_tag_name(
    'td'
)[0].find_element_by_xpath('a').click()
sleep(5)
driver.close()

# ! Send command to console
send_console_response = requests.post(
    f'{BASE_URL}/api/v0/user/{USERNAME}/consoles/{console_id}/send_input/',
    headers=HEADERS, json={'input': 'workon venv\npython3 Bot.py\n'}
)

# ! Check in success
if send_console_response.status_code in (200, 201):
    pprint(send_console_response.json())
else:
    print(send_console_response.status_code)
