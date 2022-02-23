import pandas as pd
import pymongo
from pymongo.errors import *

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['db_vacancies']
vacancies = db.vacancies

wish = int(input('Enter desired salary in roubles:'))

data_to_find = {'$or':[{'$and': [{'min_salary':{'$gte':wish}}, {'currency':'руб'}]},
                       {'$and': [{'min_salary':{'$gte':wish/80}}, {'currency':'USD'}]},
                       {'$and': [{'min_salary':{'$gte':wish/90}}, {'currency':'EUR'}]},
                       {'$and': [{'max_salary':{'$gte':wish}}, {'currency':'руб'}]},
                       {'$and': [{'max_salary':{'$gte':wish/80}}, {'currency':'USD'}]},
                       {'$and': [{'max_salary':{'$gte':wish/90}}, {'currency':'EUR'}]}
                ]}


vac_to_show = pd.DataFrame(list(vacancies.find(data_to_find)))

print(vac_to_show)