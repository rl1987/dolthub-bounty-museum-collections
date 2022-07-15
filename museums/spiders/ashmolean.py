import scrapy


class AshmoleanSpider(scrapy.Spider):
    name = 'ashmolean'
    allowed_domains = ['collections.ashmolean.org']
    start_urls = ['https://collections.ashmolean.org/collection/browse-9148']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        for url in response.xpath('//ul[@class="vr-list"]/li/a/@href').getall():
            yield scrapy.Request(url, callback=self.parse_object_page)

        next_page_url = response.xpath('//a[@class="next-btn"]/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        pass
