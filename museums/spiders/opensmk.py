import scrapy


class OpensmkSpider(scrapy.Spider):
    name = 'opensmk'
    allowed_domains = ['open.smk.dk']
    start_urls = ['http://open.smk.dk/']

    def parse(self, response):
        pass
