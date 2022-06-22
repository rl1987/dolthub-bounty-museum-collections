import scrapy

from urllib.parse import urljoin

class VictoriaSpider(scrapy.Spider):
    name = 'victoria'
    allowed_domains = ['museumsvictoria.com.au']
    start_urls = ['https://collections.museumsvictoria.com.au/search?query=&page=1&perpage=100']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        object_links = response.xpath('//div[@id="maincontent"]/div/a/@href').getall()
        for object_link in object_links:
            url = urljoin(response.url, object_link)
            yield scrapy.Request(url, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[@title="Next page"]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)


    def parse_object_page(self, response):
        pass
