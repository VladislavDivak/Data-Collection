# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from scrapy.pipelines.images import ImagesPipeline

class OlxKzPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.olx_db

    def process_item(self, item, spider):
        item['photos'] = [i['path'] for i in item['photos']]
        collection = self.mongo_base[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            collection.update_one({'_id': item['_id']}, {'$set':{'price': item['price']}})
        return item


class OlxKzPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{item["_id"]}/{item["name"]}'