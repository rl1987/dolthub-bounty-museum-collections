import scrapy


class HermitageSpider(scrapy.Spider):
    name = 'hermitage'
    allowed_domains = ['hermitagemuseum.org']
    start_urls = ['http://hermitagemuseum.org/']

    def parse(self, response):
        pass
