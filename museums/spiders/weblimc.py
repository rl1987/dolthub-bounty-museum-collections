import scrapy


class WeblimcSpider(scrapy.Spider):
    name = 'weblimc'
    allowed_domains = ['www.salsah.org']
    start_urls = ['http://www.salsah.org/']

    def parse(self, response):
        pass
