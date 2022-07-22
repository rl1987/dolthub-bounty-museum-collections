import scrapy


class NgagovauSpider(scrapy.Spider):
    name = 'ngagovau'
    allowed_domains = ['searchthecollection.nga.gov.au']
    start_urls = ['http://searchthecollection.nga.gov.au/']

    def parse(self, response):
        pass
