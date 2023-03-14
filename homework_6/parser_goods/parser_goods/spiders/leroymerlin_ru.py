import scrapy
from scrapy.http import HtmlResponse
from parser_goods.items import ParserGoodsItem
from scrapy.loader import ItemLoader


class LeroymerlinRuSpider(scrapy.Spider):
    name = "leroymerlin_ru"
    allowed_domains = ["leroymerlin.ru"]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        self.start_urls = [f"=https://vladivostok.leroymerlin.ru/search/?q=ламинат"]

    def parse(self, response:HtmlResponse):
        pages_links = response.xpath("//a[@data-qa='product-name']/@href")
        for link in pages_links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=ParserGoodsItem(), response=response)

        loader.add_xpath('name', "//h1/span/text()")
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//showcase-price-view[@slot='primary-price']/span[@slot='price']/text()")
        loader.add_xpath('photos', "//media-carousel/picture/img/@src")
        yield loader.load_item()
