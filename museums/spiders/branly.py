import scrapy


class BranlySpider(scrapy.Spider):
    name = 'branly'
    allowed_domains = ['www.quaibranly.fr']
    start_urls = ['http://www.quaibranly.fr/']

    def parse(self, response):
        pass
