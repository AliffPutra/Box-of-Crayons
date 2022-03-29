# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def remove_currency(text):
    return float(text.replace('$', ''))


class DaGroup7Item(scrapy.Item):
    # define the fields for your item here like:
    imageURL = scrapy.Field()
    sku = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(input_processor=MapCompose(remove_tags),
                        output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, remove_currency),
                        output_processor=TakeFirst())
