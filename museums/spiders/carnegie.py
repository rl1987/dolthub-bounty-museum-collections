import scrapy


class CarnegieSpider(scrapy.Spider):
    name = 'carnegie'
    allowed_domains = ['collection.cmoa.org']
    start_urls = ['http://collection.cmoa.org/']

    def parse(self, response):
        pass
