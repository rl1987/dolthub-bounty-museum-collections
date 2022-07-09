import scrapy


class ArtsAndCultureSpider(scrapy.Spider):
    name = 'artsandculture'
    allowed_domains = ['artsandculture.google.com']
    start_urls = ['http://artsandculture.google.com/']

    def parse(self, response):
        pass
