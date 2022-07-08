import scrapy


class BostonFineArtsSpider(scrapy.Spider):
    name = 'bostonfinearts'
    allowed_domains = ['collections.mfa.org']
    start_urls = ['http://collections.mfa.org/']

    def parse(self, response):
        pass
