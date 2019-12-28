import json
import requests


HEADERS_POST = {
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.heroku+json; version=3'
}
HEADERS_GET = {
    'Accept': 'application/vnd.heroku+json; version=3'
}
# payload = {
#     'name': None,
#     'region': 'us',
#     'stack': 'cedar-14'
# }
response = requests.post('https://api.heroku.com/apps/stormy-dawn-27611/sources', headers=HEADERS_POST)

# response = requests.get('https://api.heroku.com/apps/stormy-dawn-27611', headers=HEADERS_GET)
print(response.json())