import scrapy


class PennSpider(scrapy.Spider):
    name = 'penn'
    allowed_domains = ['penn.museum/']
    start_urls = ['http://penn.museum//']

    def parse(self, response):
        pass
