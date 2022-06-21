import scrapy


class BritishmuseumSpider(scrapy.Spider):
    name = 'britishmuseum'
    allowed_domains = ['britishmuseum.org']
    start_urls = ['http://britishmuseum.org/']

    def parse(self, response):
        pass
