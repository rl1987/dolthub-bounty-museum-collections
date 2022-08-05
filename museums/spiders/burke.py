import scrapy


class BurkeSpider(scrapy.Spider):
    name = 'burke'
    allowed_domains = ['www.burkemuseum.org']
    start_urls = ['https://www.burkemuseum.org/collections-and-research/culture/contemporary-culture/database/browse.php']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_art_collection_page)

    def parse_art_collection_page(self, response):
        for l in response.xpath('//td[@class="collectionsText"]/a/@href').getall():
            yield response.follow(l, callback=self.parse_art_collection_page)

        for l in response.xpath('//td[@class="resultsData"]/a/@href').getall():
            yield response.follow(l, callback=self.parse_artwork_page)

    def parse_artwork_page(self, response):
        pass
