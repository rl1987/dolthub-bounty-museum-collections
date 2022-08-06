import scrapy


class EuropeanaSpider(scrapy.Spider):
    name = 'europeana'
    allowed_domains = ['api.europeana.eu']
    start_urls = ['http://api.europeana.eu/']

    def parse(self, response):
        pass
