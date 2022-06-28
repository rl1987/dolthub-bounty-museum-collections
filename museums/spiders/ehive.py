import scrapy


class EhiveSpider(scrapy.Spider):
    name = 'ehive'
    allowed_domains = ['ehive.com']
    start_urls = ['http://ehive.com/']

    def parse(self, response):
        pass
