import scrapy


class MucemSpider(scrapy.Spider):
    name = 'mucem'
    allowed_domains = ['www.mucem.org']
    start_urls = ['http://www.mucem.org/']

    def parse(self, response):
        pass
