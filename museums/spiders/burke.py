import scrapy


class BurkeSpider(scrapy.Spider):
    name = 'burke'
    allowed_domains = ['www.burkemuseum.org']
    start_urls = ['http://www.burkemuseum.org/']

    def parse(self, response):
        pass
