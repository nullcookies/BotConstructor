import json
import requests


# SOURCE_HEADERS = {
#     'Content-Type': 'application/json',
#     'Accept': 'application/vnd.heroku+json; version=3'
# }
AUTH_TOKEN = 'c7621267-7a35-438f-86af-dc4cdb48724b'
file = open(r'C:\Users\user\Desktop\ForHeroku\TestBot.py', 'rb').read()

PUT_HEADERS = {
    'Content-type': f'{file}',
    'Authorization': 'Bearer ' + AUTH_TOKEN
}
headers = {
    'Accept': 'application/vnd.heroku+json; version=3',
    'Authorization': 'Bearer ' + AUTH_TOKEN,
    'Content-type': 'application/json'
}
payload = {
    'source_blob': {
        'get_url': 'https://s3-external-1.amazonaws.com/heroku-sources-production/2868901c-a29e-4d3f-a49a-0e4cec6dd014?AWSAccessKeyId=AKIAJ6LKZGKGPARPZE4A&Signature=ejkaM5vemuEWSZhHinla3dpSA3Q%3D&Expires=1579118126',
        'put_url': 'https://s3-external-1.amazonaws.com/heroku-sources-production/2868901c-a29e-4d3f-a49a-0e4cec6dd014?AWSAccessKeyId=AKIAJ6LKZGKGPARPZE4A&Signature=hUXFvEBbbammZFlNO3p7jkc2Fg4%3D&Expires=1579118126'
    }
}

# source_response = requests.put(payload['source_blob']['put_url'],
#                                headers=headers, data=f'{file}')
# print(source_response.status_code)

# Client:      <none>
# ID:          919f4ff0-f6de-438c-8a69-161abe4258e1
# Description: Long-lived user authorization
# Scope:       global
# Token:       f4245d04-598f-4823-ae4a-bf5de13c4675
# Updated at:  Fri Jan 17 2020 10:52:46 GMT+0200 (Eastern European Standard Time) (less than a minute ago)


url = 'https://api.heroku.com/apps/stormy-dawn-27611/sources'

headers = {
    'Accept': 'application/vnd.heroku+json; version=3',
    'Authorization': 'Bearer ' + AUTH_TOKEN,
    'Content-Type': 'application/json'
}


get_url = 'https://s3-external-1.amazonaws.com/heroku-sources-production/2868901c-a29e-4d3f-a49a-0e4cec6dd014?AWSAccessKeyId=AKIAJ6LKZGKGPARPZE4A&Signature=ejkaM5vemuEWSZhHinla3dpSA3Q%3D&Expires=1579118126',
put_url = 'https://s3-external-1.amazonaws.com/heroku-sources-production/2868901c-a29e-4d3f-a49a-0e4cec6dd014?AWSAccessKeyId=AKIAJ6LKZGKGPARPZE4A&Signature=hUXFvEBbbammZFlNO3p7jkc2Fg4%3D&Expires=1579118126'

files = {
    'TestBot.py': open(r'C:\Users\user\Desktop\ForHeroku\TestBot.py', 'rb')
}


h2 = {'Authorization': 'Bearer ' + AUTH_TOKEN}
put_response = requests.put(put_url, data=files, headers=headers)
print(put_response.content, put_response.status_code)
