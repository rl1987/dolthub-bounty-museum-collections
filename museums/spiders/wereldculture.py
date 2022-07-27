import scrapy


class WereldcultureSpider(scrapy.Spider):
    name = 'wereldculture'
    allowed_domains = ['collectie.wereldculturen.nl']
    start_urls = ['http://collectie.wereldculturen.nl/']

    def parse(self, response):
        pass
