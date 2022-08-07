import scrapy


class MuseumseuSpider(scrapy.Spider):
    name = 'museumseu'
    allowed_domains = ['museums.eu']
    start_urls = ['http://museums.eu/search/index?documenttype=collection&page=1']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_collection_list)

    def parse_collection_list(self, response):
        for l in response.xpath('//h4[@class="media-heading"]/a/@href').getall():
            yield response.follow(l, callback=self.parse_object_list)

        for l in response.xpath('//ul[@class="pagination"]/li/a/@href'):
            yield response.follow(l, callback=self.parse_collection_list)

    def parse_object_list(self, response):
        for l in response.xpath('//div[@class="artwork"]/a/@href').getall():
            yield response.follow(l, callback=self.parse_object_page)

        for l in response.xpath('//ul[@id="collection-pagination"]/li/a/@href').getall():
            yield response.follow(l, callback=self.parse_object_list)

    def parse_object_page(self, response):
        pass
