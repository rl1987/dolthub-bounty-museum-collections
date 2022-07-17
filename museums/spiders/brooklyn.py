import scrapy


class BrooklynSpider(scrapy.Spider):
    name = 'brooklyn'
    allowed_domains = ['brooklynmuseum.org']
    start_urls = ['https://www.brooklynmuseum.org/opencollection/search?type=objects&limit=12&offset=0']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        for url in response.xpath('//div[contains(@class, "item-content")]/a/@href').getall():
            yield scrapy.Request(url, callback=self.parse_object_page)

        next_page_url = response.xpath('//a[./i[@class="icon-right-open"]]/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        pass
