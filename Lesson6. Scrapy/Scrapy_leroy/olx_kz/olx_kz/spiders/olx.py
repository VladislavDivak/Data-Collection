import scrapy
from scrapy.http import HtmlResponse
import time
from olx_kz.items import OlxKzItem
from scrapy.loader import ItemLoader

class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ['olx.kz']
    start_urls = ['https://www.olx.kz/nedvizhimost/kvartiry/']

    def parse(self, response: HtmlResponse):
        # The next page is represented by a dynamically-generated button. I couldn't find any solution, how scrapy can just click the button like selenium
        next_page = response.xpath('//a[@data-cy="page-link-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//td[@class="photo-cell"]/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=OlxKzItem(), response=response)
        loader.add_xpath('name', "//h1//text()")
        loader.add_xpath('price', "//h3/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('photos', '//div[@class="swiper-zoom-container"]/img/@data-src | //div[@class="swiper-zoom-container"]/img/@src')
        yield loader.load_item()
        #name = response.xpath("//h1//text()").get()
        #price = response.xpath("//h3/text()").get()
        #url = response.url
        #photos = response.xpath('//div[@class="swiper-zoom-container"]/img/@data-src | //div[@class="swiper-zoom-container"]/img/@src').getall()
        #yield AvitoparserItem(name=name, price=price, url=url, photos=photos)
