import scrapy


class MuseumseuSpider(scrapy.Spider):
    name = 'museumseu'
    allowed_domains = ['museums.eu']
    start_urls = ['http://museums.eu/']

    def parse(self, response):
        pass
