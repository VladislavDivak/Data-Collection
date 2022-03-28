from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from l6_jobparser import settings
from l6_jobparser.spiders.hhru import HhruSpider
from l6_jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    #process.crawl(HhruSpider)
    process.crawl(SjruSpider)

    process.start()

