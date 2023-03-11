# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserJobItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    source = scrapy.Field()
    _id = scrapy.Field()

