import scrapy

from urllib.parse import urljoin

class PennSpider(scrapy.Spider):
    name = 'penn'
    allowed_domains = ['www.penn.museum']
    start_urls = ['https://www.penn.museum/collections/search.php?term=&submit_term=Submit+Query&type%5B%5D=1']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_results)

    def parse_search_results(self, response):
        for object_link in response.xpath('//a[./img[contains(@class, "center-block")]]/@href').getall():
            object_url = urljoin(response.url, object_link) 
            yield scrapy.Request(object_url, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[text()="Next"]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_search_results)

    def parse_object_page(self, response):
        pass
