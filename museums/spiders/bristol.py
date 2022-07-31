import scrapy


class BristolSpider(scrapy.Spider):
    name = 'bristol'
    allowed_domains = ['museums.bristol.gov.uk']
    start_urls = ['http://museums.bristol.gov.uk/']

    def parse(self, response):
        pass
