import scrapy


class ScienceSpider(scrapy.Spider):
    name = 'science'
    allowed_domains = ['collection.sciencemuseumgroup.org.uk']
    start_urls = ['https://collection.sciencemuseumgroup.org.uk/search/objects']

    def parse(self, response):
        pass
