import scrapy


class NpglondonSpider(scrapy.Spider):
    name = 'npglondon'
    allowed_domains = ['www.npg.org.uk']
    start_urls = ['http://www.npg.org.uk/']

    def parse(self, response):
        pass
