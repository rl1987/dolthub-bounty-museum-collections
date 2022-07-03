import scrapy


class SeamusemSpider(scrapy.Spider):
    name = 'seamusem'
    allowed_domains = ['sea.museum']
    start_urls = ['http://sea.museum/']

    def parse(self, response):
        pass
