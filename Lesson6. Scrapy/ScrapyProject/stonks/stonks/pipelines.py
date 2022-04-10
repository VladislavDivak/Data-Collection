# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class StonksPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.stonksdb

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            collection.update_one({'_id': item['_id']},
                                  {'$set':{'price': item['price']}},
                                  {'$set':{'p_e': item['p_e']}},
                                  {'$set':{'d_e': item['d_e']}},
                                  {'$set':{'market_cap': item['market_cap']}},
                                  {'$set':{'oper_margin': item['oper_margin']}},
                                  {'$set':{'ebitda': item['ebitda']}})
        return item

