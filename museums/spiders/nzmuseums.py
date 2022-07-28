import scrapy


class NzmuseumsSpider(scrapy.Spider):
    name = 'nzmuseums'
    allowed_domains = ['www.nzmuseums.co.nz']
    start_urls = ['http://www.nzmuseums.co.nz/']

    def parse(self, response):
        pass
