import scrapy

class BostonFineArtsSpider(scrapy.Spider):
    name = 'bostonfinearts'
    allowed_domains = ['collections.mfa.org']
    start_urls = ['https://collections.mfa.org/search/objects/*/*']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        links = response.xpath('//div[@class="grid-item-inner"]//h3/a/@href').getall()
        for l in links:
            yield response.follow(l, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[contains(@class, "next-page-link")]/@href').get()
        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse_search_page)

    def parse_object_page(self, response):
        pass
