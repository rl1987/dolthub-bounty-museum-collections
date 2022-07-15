import scrapy


class AshmoleanSpider(scrapy.Spider):
    name = 'ashmolean'
    allowed_domains = ['collections.ashmolean.org']
    start_urls = ['https://collections.ashmolean.org/collection/browse-9148']

    def parse(self, response):
        pass
