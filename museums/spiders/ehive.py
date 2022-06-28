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
        institution_name = response.xpath("//title/text()").get().replace(" on eHive", "")
        institution_latitude = response.xpath('//span[@id="latitude"]/text()').get()
        institution_longitude = response.xpath('//span[@id="longitude"]/text()').get()

        meta = {
            'institution_name': institution_name,
            'institution_latitude': institution_latitude,
            'institution_longitude': institution_longitude
        }
                

        # TODO: come up with a way to remove data from what appears to be test profiles
        view_all_link = response.xpath('//h5[text()="Entire collection - "]/a/@href').get()
        view_all_url = urljoin(response.url, view_all_link)
        yield scrapy.Request(view_all_url, callback=self.parse_object_list, meta=meta)

    def parse_object_list(self, response):
        meta = {
            'institution_name': response.meta.get('institution_name'),
            'institution_latitude': response.meta.get('institution_latitude'),
            'institution_longitude': response.meta.get('institution_longitude')
        }

        for object_link in response.xpath('//a[./img[@class="eh-image"]]/@href').getall():
            object_url = urljoin(response.url, object_link)
            yield scrapy.Request(object_url, callback=self.parse_object_page, meta=meta)

        next_page_link = response.xpath('//a[@aria-label="Next"]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_object_list, meta=meta)

    def parse_object_page(self, response):
        self.logger.debug(response.meta)

