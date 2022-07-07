import scrapy


class AucklandSpider(scrapy.Spider):
    name = 'auckland'
    allowed_domains = ['aucklandmuseum.com']
    start_urls = ['http://aucklandmuseum.com/']

    def parse(self, response):
        pass
