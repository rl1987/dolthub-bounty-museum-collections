import scrapy

import string

class NpglondonSpider(scrapy.Spider):
    name = 'npglondon'
    allowed_domains = ['www.npg.org.uk']
    start_urls = [ "https://www.npg.org.uk/collections/search/arta-z/?index=" + letter for letter in string.ascii_lowercase ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_artist_list)

    def parse_artist_list(self, response):
        for l in response.xpath('//div[@id="eventsListing"]/p/a/@href').getall():
            yield response.follow(l, callback=self.parse_portrait_list)

    def parse_portrait_list(self, response):
        for l in response.xpath('//p[@class="eventHeading"]/a/@href').getall():
            yield response.follow(l, callback=self.parse_portrait_page)

    def parse_portrait_page(self, response):
        pass

