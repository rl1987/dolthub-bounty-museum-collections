import scrapy


class AlbertinaSpider(scrapy.Spider):
    name = 'albertina'
    allowed_domains = ['sammlungenonline.albertina.at']
    start_urls = ['http://sammlungenonline.albertina.at/']

    def parse(self, response):
        pass
