import scrapy


class CentrepompidouSpider(scrapy.Spider):
    name = 'centrepompidou'
    allowed_domains = ['www.centrepompidou.fr']
    start_urls = ['http://www.centrepompidou.fr/']

    def parse(self, response):
        pass
