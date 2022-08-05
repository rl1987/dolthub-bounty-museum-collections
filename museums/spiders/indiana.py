import scrapy


class IndianaSpider(scrapy.Spider):
    name = 'indiana'
    allowed_domains = ['collection.indianamuseum.org']
    start_urls = ['http://collection.indianamuseum.org/']

    def parse(self, response):
        pass
