import scrapy


class VictoriaSpider(scrapy.Spider):
    name = 'victoria'
    allowed_domains = ['museumsvictoria.com.au']
    start_urls = ['http://museumsvictoria.com.au/']

    def parse(self, response):
        pass
