import requests
import json

API_KEY = '05a7cae2-c60d-4d1b-a4a8-5554d3e93e08'
BASE_URL = 'https://holidayapi.com/v1/holidays'


class Contries:
    def __init__(self, name_file):
        self.name_file = name_file

    def get_countries_names(self):
        with open(self.name_file, 'r') as file_name:
            info = file_name.read().splitlines()
            data = {}
            for line in info:
                line_split = line.split()
                data[line_split[1]] = line_split[0]
        return data


class Holiday:
    def __init__(self, key, data_dict):
        self.key = key
        self.data_dict = data_dict
        self.base_url = BASE_URL

    def get_holidays(self, name):
        for contry, index in self.data_dict.items():
            if name == contry:
                conty_index = index
                break

        parameters = {'key': self.key, 'country': conty_index, 'year': '2018'}
        respone = requests.get(self.base_url, params=parameters)
        return respone.json()

    def save_to_json(self, data_dict):
        with open('contries_json.json', 'w', encoding='utf-8') as file_name:
            json.dump(data_dict['holidays'], file_name, indent=4, ensure_ascii=False)


cont = Contries('contries.txt')

contry = input('Enter contry to get all holidays: ')
hol = Holiday(API_KEY, cont.get_countries_names())
hol.save_to_json(hol.get_holidays(contry))
