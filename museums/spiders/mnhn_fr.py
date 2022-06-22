import scrapy


class MnhnFrSpider(scrapy.Spider):
    name = 'mnhn_fr'
    allowed_domains = ['science.mnhn.fr']
    start_urls = ['http://science.mnhn.fr/']

    def parse(self, response):
        pass
