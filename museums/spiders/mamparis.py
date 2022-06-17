import scrapy


class MamparisSpider(scrapy.Spider):
    name = 'mamparis'
    allowed_domains = ['mam.paris.fr']
    start_urls = ['http://mam.paris.fr/']

    def parse(self, response):
        pass
