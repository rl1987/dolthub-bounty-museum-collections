import scrapy

from urllib.parse import urljoin

class EhiveSpider(scrapy.Spider):
    name = 'ehive'
    allowed_domains = ['ehive.com']
    start_urls = ['https://ehive.com/collections']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_collection_list)

    def parse_collection_list(self, response):
        for museum_link in response.xpath('//a[@class="eh-summary-account-record-profile-name"]/@href').getall():
            museum_url = urljoin(response.url, museum_link)
            yield scrapy.Request(museum_url, callback=self.parse_museum_page)

        next_page_link = response.xpath('//a[@aria-label="Next"]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_collection_list)

    def parse_museum_page(self, response):
        institution_name = response.xpath('//span[@id="publicProfileName"]/text()').get()
        institution_latitude = response.xpath('//span[@id="latitude"]/text()').get()
        institution_longitude = response.xpath('//span[@id="longitude"]/text()').get()

        view_all_link = response.xpath('//h5[text()="Entire collection - "]/a/@href').get()
        view_all_url = urljoin(response.url, view_all_link)
        yield scrapy.Request(view_all_url, callback=self.parse_object_list)

    def parse_object_list(self, response):
        pass

    def parse_object_page(self, response):
        pass
