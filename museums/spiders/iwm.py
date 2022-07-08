import scrapy

from urllib.parse import urljoin

class IwmSpider(scrapy.Spider):
    name = 'iwm'
    allowed_domains = ['iwm.org.uk']
    start_urls = ['https://www.iwm.org.uk/collections/search?query=&pageSize=30&media-records=all-records&page=1']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        links = response.xpath('//div[@class="teaser-list__title--content"]/a/@href').getall()
        for l in links:
            url = urljoin(response.url, l)
            yield scrapy.Request(url, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[@title="Go to next page"]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        pass
