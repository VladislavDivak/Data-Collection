import scrapy
from scrapy.http import HtmlResponse
from l6_jobparser.items import L6JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Br%5D%5B0%5D=2',
                  'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Br%5D%5B0%5D=3',
                  'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Br%5D%5B0%5D=4',
                  'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Br%5D%5B0%5D=5',
                  'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Br%5D%5B0%5D=6']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[contains(@class,"f-test-link-Dalshe")]//@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//span[@class="_1BiPY _26ig7 _1d47O"]//@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').get()
        salary = response.xpath("//span[@class = '_2Wp8I _1BiPY _26ig7 _18w_0']/text()").getall()
        link = response.url
        item = L6JobparserItem(name=name, salary=salary, link=link)
        yield item