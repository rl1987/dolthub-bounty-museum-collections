import scrapy


class AnthroSpider(scrapy.Spider):
    name = 'anthro'
    allowed_domains = ['anthro.amnh.org']
    start_urls = ['http://anthro.amnh.org/']

    def parse(self, response):
        pass
