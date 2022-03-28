# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class L6JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy0712

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['min'], item['max'], item['cur'] = self.process_salary_hhru(item['salary'])
            del item['salary']
        if spider.name == 'sjru':
            item['min'], item['max'], item['cur'] = self.process_salary_sjru(item['salary'])
            del item['salary']

        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hhru(self, salary):
        try:
            if salary[0] == 'до ':
                min = None
                max = int(salary[1].replace('\xa0', ''))
            elif salary[0] == 'от ' and salary[2] == ' до ':
                min = int(salary[1].replace('\xa0', ''))
                max = int(salary[3].replace('\xa0', ''))
            else:
                min = int(salary[1].replace('\xa0', ''))
                max = None
            cur = salary[-1].replace('.', '')
        except:
            min = None
            max = None
            cur = None

        return min, max, cur

    def process_salary_sjru(self, salary):
        try:
            if salary[0] == 'до':
                min = None
                max = int("".join(salary[2].replace('\xa0',' ').split()[:2]))
                cur = salary[2].replace('\xa0',' ').split()[2].replace('.', '')
            elif salary[0] == 'от':
                min = int("".join(salary[2].replace('\xa0',' ').split()[:2]))
                max = None
                cur = salary[2].replace('\xa0', ' ').split()[2].replace('.', '')
            else:
                min = int(salary[0].replace('\xa0', ''))
                max = int(salary[2].replace('\xa0', ''))
                cur = salary[3].replace('.', '')
        except:
            min = None
            max = None
            cur = None

        return min, max, cur