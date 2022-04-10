# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import MapCompose, TakeFirst
import scrapy

def clear_value(value):
    if value[-1] == "B":
        value = value.removesuffix('B')
        return float(value)*1000
    elif value[-1] == "M" or value[-1] == "%":
        value = value.removesuffix(value[-1])
        return float(value)
    else:
        try:
            return float(value)
        except:
            return value


class StonksItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field(output_processor=TakeFirst())
    ticker = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    company_website = scrapy.Field(output_processor=TakeFirst())
    sector = scrapy.Field(output_processor=TakeFirst())
    country = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_value))
    market_cap = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_value))
    p_e = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_value))
    d_e = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_value))
    oper_margin = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_value))
    ebitda = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_value))


