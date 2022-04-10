import scrapy
from scrapy.http import HtmlResponse
from stonks.items import StonksItem
from scrapy.loader import ItemLoader


class FinvizSpider(scrapy.Spider):
    name = 'finviz'
    allowed_domains = ['finviz.com']
    start_urls = ['https://finviz.com/screener.ashx?v=161']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('(//a[@class="tab-link" and position() = last()])[2]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@class="screener-link-primary"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.stonks_parse)

    def stonks_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=StonksItem(), response=response)
        loader.add_xpath('ticker', '//a[@class="fullview-ticker"]/text()')
        loader.add_xpath('name', '(//table[@class="fullview-title"]//tr)[2]//text()')
        loader.add_xpath('company_website', '(//table[@class="fullview-title"]//tr)[2]//@href')
        loader.add_xpath('sector', '(//td[@class="fullview-links"]/a)[1]/text()')
        loader.add_xpath('country', '(//td[@class="fullview-links"]/a)[3]/text()')
        loader.add_xpath('price', '((//tr[@class="table-dark-row"])[11]/td)[12]//text()')
        loader.add_xpath('market_cap', '((//tr[@class="table-dark-row"])[2]/td)[2]//text()')
        loader.add_xpath('p_e', '((//tr[@class="table-dark-row"])[1]/td)[4]//text()')
        loader.add_xpath('d_e', '((//tr[@class="table-dark-row"])[10]/td)[4]//text()')
        loader.add_xpath('oper_margin', '((//tr[@class="table-dark-row"])[9]/td)[8]//text()')
        loader.add_xpath('ebitda', '((//tr[@class="table-dark-row"])[17]/td)[3]//text()')

        yield loader.load_item()

        #ticker = response.xpath('//a[@class="fullview-ticker"]/text()').get()
        #name = response.xpath('(//table[@class="fullview-title"]//tr)[2]//text()').get()
        #company_website = response.xpath('(//table[@class="fullview-title"]//tr)[2]//@href').get()
        #sector = response.xpath('(//td[@class="fullview-links"]/a)[1]/text()').get()
        #country = response.xpath('(//td[@class="fullview-links"]/a)[3]/text()').get()
        #price = response.xpath('((//tr[@class="table-dark-row"])[11]/td)[12]//text()').get()
        #market_cap = response.xpath('((//tr[@class="table-dark-row"])[2]/td)[2]//text()').get()
        #p_e = response.xpath('((//tr[@class="table-dark-row"])[1]/td)[4]//text()').get()
        #d_e = response.xpath('((//tr[@class="table-dark-row"])[10]/td)[4]//text()').get()
        #oper_margin = response.xpath('((//tr[@class="table-dark-row"])[9]/td)[8]//text()').get()
        #ebitda = response.xpath('((//tr[@class="table-dark-row"])[17]/td)[3]//text()').get()

        #item = L6JobparserItem(name=name, salary=salary, link=link)
        #yield item
