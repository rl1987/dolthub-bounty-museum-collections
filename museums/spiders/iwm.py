import scrapy


class IwmSpider(scrapy.Spider):
    name = 'iwm'
    allowed_domains = ['iwm.org.uk']
    start_urls = ['http://iwm.org.uk/']

    def parse(self, response):
        pass
