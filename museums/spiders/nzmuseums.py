import scrapy


class NzmuseumsSpider(scrapy.Spider):
    name = 'nzmuseums'
    allowed_domains = ['www.nzmuseums.co.nz']
    start_urls = ['https://www.nzmuseums.co.nz/objects?view=lightbox']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        for artwork_link in response.xpath('//div[@class="lightbox-object-desc "]/a/@href'):
            yield response.follow(artwork_link, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[@aria-label="Next"]/@href').get()
        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse_search_page)

    def parse_object_page(self, response):
        pass
