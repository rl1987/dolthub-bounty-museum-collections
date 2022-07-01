import scrapy


class VictoriaNAlbertSpider(scrapy.Spider):
    name = 'victorianalbert'
    allowed_domains = ['api.vam.ac.uk']
    start_urls = ['http://api.vam.ac.uk/']

    def parse(self, response):
        pass
