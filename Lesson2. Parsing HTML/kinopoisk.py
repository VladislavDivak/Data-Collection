# https://www.kinopoisk.ru/popular/films/?quick_filters=serials&tab=all

import requests
from bs4 import BeautifulSoup as BS
from pprint import pprint

url = 'https://www.kinopoisk.ru'

suffix = '/popular/films/'

params = {'quick_filters': 'serials',
          'tab': 'all',
           'page': 1}

headers = {'User-Agent': 'Chrome/98.0.4758.102'}

response = requests.get(url + suffix, params=params, headers=headers)
dom = BS(response.text, 'html.parser')

# with open('1.html', 'w') as f:
#     f.write(dom.text)

serials = dom.find_all('div', {'class':'desktop-rating-selection-film-item__upper-wrapper'})

serial_list = []

for serial in serials:
    serial_data = {}
    name = serial.find('p').text
    link = url + serial.find('p').parent.get('href')
    rating = serial.find('span', {'class': 'rating film-item-user-data__rating'}).find('span').text
    try:
        rating = float(rating)
    except:
        rating = None

    serial_data['name'] = name
    serial_data['link'] = link
    serial_data['rating'] = rating

    serial_list.append(serial_data)

pprint(serial_list)
print()