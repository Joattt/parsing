# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst


class ParserGoodsItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    photos = scrapy.Field()
    _id = scrapy.Field()
