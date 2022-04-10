import pandas as pd
import pymongo
from pymongo.errors import *

client = pymongo.MongoClient('localhost', 27017)
mongobase = client.stonksdb
collection = mongobase['FinvizSpider']

data_to_find = {'min_salary':{'$lte':80}}

shares_to_show = pd.DataFrame(list(collection.find(data_to_find)))

print(shares_to_show)