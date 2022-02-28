import requests
from lxml import html
import pandas as pd
import pymongo
from pprint import pprint
from pymongo.errors import *

###Creating the database
client = pymongo.MongoClient('127.0.0.1', 27017)
db = client['db_news']
news = db.news

#Data to enter the needed profession in
url = 'https://news.mail.ru/'
headers = {'User-Agent': 'Chrome/98.0.4758.102'}
response = requests.get(url, headers=headers)
root = html.fromstring(response.text)

titles_in_pic = root.xpath("//span[contains(@class,'photo__title')]/text()")[:3]
titles_in_list = root.xpath("//a[@class='list__text']/text()")
titles_in_list2 = root.xpath("//a[contains(@class,'link_flex')]/span/text()")
titles_with_pic = root.xpath("//span[@class='newsitem__title-inner']/text()")

links_in_pic = root.xpath("//span[contains(@class,'photo__title')]/../../@href")[:3]
links_in_list = root.xpath("//a[@class='list__text']/@href")
links_in_list2 = root.xpath("//a[contains(@class,'link_flex')]/@href")
links_with_pic = root.xpath("//span[@class='newsitem__title-inner']/../@href")

source_with_pic = root.xpath("//span[@class='newsitem__param']/text()")
date_with_pic = root.xpath("//span[contains(@class,'js-ago')]/@datetime")

blocks = [[titles_in_pic, links_in_pic],
         [titles_in_list, links_in_list],
         [titles_in_list2, links_in_list2],
         [titles_with_pic, links_with_pic, source_with_pic, date_with_pic]]

news_list = []

for block in blocks:
    for i in range(len(block[0])):
        news_item = {}

        news_item['_id'] = block[1][i] #here lies link
        news_item['title'] = block[0][i].replace('\xa0', ' ')
        news_item['link'] = block[1][i]
        try:
            news_item['source'] = block[2][i]
            news_item['date'] = block[3][i]
        except:
            news_item['source'] = None
            news_item['date'] = None

        news_list.append(news_item)

for n in news_list:
    try:
        news.insert_one(n)
    except:
        pass

news_to_show = pd.DataFrame(list(news.find()))

news_to_show
print()