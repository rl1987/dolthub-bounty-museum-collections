import scrapy

from urllib.parse import urljoin

class SeamusemSpider(scrapy.Spider):
    name = 'seamusem'
    allowed_domains = ['sea.museum']
    start_urls = ['http://collections.sea.museum/search/*/objects?filter=MediaExistence%3Atrue#filters',
            'http://collections.sea.museum/search/*/objects?filter=MediaExistence%3Afalse']

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        for object_link in response.xpath('//a[starts-with(@href, "/objects/")]/@href').getall():
            object_url = urljoin(response.url, object_link)
            yield scrapy.Request(object_url, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[contains(@class, "next-page-link")]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        pass
