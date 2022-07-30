import scrapy


class CambridgemaaSpider(scrapy.Spider):
    name = 'cambridgemaa'
    allowed_domains = ['collections.maa.cam.ac.uk']
    start_urls = ['http://collections.maa.cam.ac.uk/']

    def parse(self, response):
        pass
