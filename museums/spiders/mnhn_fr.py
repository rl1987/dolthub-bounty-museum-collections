import scrapy

from urllib.parse import urljoin

class MnhnFrSpider(scrapy.Spider):
    name = 'mnhn_fr'
    allowed_domains = ['science.mnhn.fr']
    start_urls = ['https://science.mnhn.fr/institution/mnhn/item/list?startIndex=0']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        item_links = response.xpath('//div[@class="title"]/a/@href').getall()

        for item_link in item_links:
            url = urljoin(response.url, item_link)
            yield scrapy.Request(url, callback=self.parse_item_page)

        next_page_link = response.xpath('//a[./i[@class="icon-arrow-right"]]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_item_page(self, response):
        pass

