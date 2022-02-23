#https://hh.ru/vacancies/data-scientist?page=0&hhtmFrom=vacancy_search_catalog
import requests
from bs4 import BeautifulSoup as bs
from transliterate import translit
import pandas as pd
import time
import pymongo
from pprint import pprint
from pymongo.errors import *

###Creating the database
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['db_vacancies']
vacancies = db.vacancies

#Function to avoid duplicates and add data to db
def db_add(db, docs):
    for doc in docs:
        try:
            db.insert_one(doc)
        except:
            pass

#Data to enter the needed profession in hh.ru
url = 'https://hh.ru/vacancies/'
suffix = str(input('Enter the profession')).replace(' ', '-')
suffix = translit(suffix, 'ru', reversed = True)
pages = int(input('How many pages to search? Type 999 to search all'))
vacancies_list = []

#function to find the data from page
def parsing(dom):
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item__row_header'})
    vac_list = []
    for vac in vacancies:
        vacancies_data = {}
        id = vac.find('a').get('href')
        name = vac.find('a', {'class': 'bloko-link'}).text
        employer = vac.find_next_sibling().find('a').text.replace('\xa0', ' ')
        link = vac.find('a').get('href')
        try:
            salary = vac.find_all('span', {'class': 'bloko-header-section-3_lite'})[1].text.replace('\u202f', '')
            if salary[:2] == 'до':
                min_salary = None
                max_salary = [int(s) for s in salary.split() if s.isdigit()][0]
                currency = salary[-4:].replace(' ', '').replace('.', '')
            elif salary[:2] == 'от':
                min_salary = [int(s) for s in salary.split() if s.isdigit()][0]
                max_salary = None
                currency = salary[-4:].replace(' ', '').replace('.', '')
            else:
                min_salary = [int(s) for s in salary.split() if s.isdigit()][0]
                max_salary = [int(s) for s in salary.split() if s.isdigit()][1]
                currency = salary[-4:].replace(' ', '').replace('.', '')
        except:
            min_salary = None
            max_salary = None
            currency = None

        vacancies_data['_id'] = id
        vacancies_data['name'] = name
        vacancies_data['employer'] = employer
        vacancies_data['link'] = link
        vacancies_data['min_salary'] = min_salary
        vacancies_data['max_salary'] = max_salary
        vacancies_data['currency'] = currency

        vac_list.append(vacancies_data)
    return vac_list

#Condition to search all pages
if pages == 999:
    params = {'hhtmFrom': 'vacancy_search_catalog',
              'page': 0}
    headers = {'User-Agent': 'Chrome/98.0.4758.102'}

    response = requests.get(url + suffix, params=params, headers=headers)
    dom = bs(response.text, 'html.parser')
    pages = int(dom.find_all('a',{'class':'bloko-button'})[-2].text)

#Iteration to go through set pages and do def parsing  (with time sleep)
for page in range(pages):
    params = {'hhtmFrom': 'vacancy_search_catalog',
               'page': page}
    headers = {'User-Agent': 'Chrome/98.0.4758.102'}

    response = requests.get(url + suffix, params=params, headers=headers)
    dom = bs(response.text, 'html.parser')
    parsing_data = parsing(dom)
    vacancies_list = vacancies_list + parsing_data
    time.sleep(2)

db_add(vacancies, vacancies_list)

vac_to_show = pd.DataFrame(list(vacancies.find()))

vac_to_show


