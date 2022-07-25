import scrapy


class DigitaltmuseumSpider(scrapy.Spider):
    name = 'digitaltmuseum'
    allowed_domains = ['digitaltmuseum.org']
    start_urls = ['http://digitaltmuseum.org/']

    def parse(self, response):
        pass
