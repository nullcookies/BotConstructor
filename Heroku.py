import json
import requests


SOURCE_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.heroku+json; version=3'
}

file = open(r'C:\Users\user\Desktop\ForHeroku.zip', 'rb').read()

PUT_HEADERS = {
    'Content-Type': file
}
payload = {
    'source_blob': {
        'get_url': 'https://s3-external-1.amazonaws.com/heroku-sources-production/2868901c-a29e-4d3f-a49a-0e4cec6dd014?AWSAccessKeyId=AKIAJ6LKZGKGPARPZE4A&Signature=ejkaM5vemuEWSZhHinla3dpSA3Q%3D&Expires=1579118126',
        'put_url': 'https://s3-external-1.amazonaws.com/heroku-sources-production/2868901c-a29e-4d3f-a49a-0e4cec6dd014?AWSAccessKeyId=AKIAJ6LKZGKGPARPZE4A&Signature=hUXFvEBbbammZFlNO3p7jkc2Fg4%3D&Expires=1579118126'
    }
}

# response = requests.post('https://api.heroku.com/apps/stormy-dawn-27611/sources', headers=HEADERS_POST)
# source_response = requests.post('https://api.heroku.com/sources',
#                                 headers=SOURCE_HEADERS, data=payload)
source_response = requests.put(payload['source_blob']['put_url'],
                               headers=PUT_HEADERS)
# response = requests.get('https://api.heroku.com/apps/stormy-dawn-27611', headers=HEADERS_GET)
print(source_response.status_code, source_response.json())
