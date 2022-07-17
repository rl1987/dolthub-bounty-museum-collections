import scrapy

from museums.items import ObjectItem

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
        item = ObjectItem()

        item['object_number'] = response.url.split('/')[-1]
        item['institution_name'] = 'Brooklyn Museum'
        item['institution_city'] = 'New York'
        item['institution_state'] = 'NY'
        item['institution_country'] = 'United States'
        item['institution_latitude'] = 40.6712062
        item['institution_longitude'] = -73.9646874
        item['department'] = response.xpath('//div[@class="tombstone-data-row" and ./strong[text()="COLLECTIONS"]]/a/text()').get()
        item['title'] = response.xpath('//h1/text()').get()
        item['description'] = " ".join(response.xpath('//div[@class="tombstone-data-row" and ./strong[text()="CATALOGUE DESCRIPTION"]]/text()').getall()).strip()
        item['current_location'] = " ".join(response.xpath('//div[@class="tombstone-data-row" and ./strong[text()="MUSEUM LOCATION"]]/text()').getall()).strip()
        item['dimensions'] = " ".join(response.xpath('//div[@class="tombstone-data-row" and ./strong[text()="DIMENSIONS"]]/text()').getall()).strip()
        item['inscription'] = " ".join(response.xpath('//div[@class="tombstone-data-row" and ./strong[text()="INSCRIPTIONS"]]/text()').getall()).strip()
        item['materials'] = " ".join(response.xpath('//div[@class="tombstone-data-row" and ./strong[text()="MEDIUM"]]/text()').getall()).strip()
        item['from_location'] = response.xpath('//li[contains(text(),"Place Made:")]/a/text()').get()
        item['culture'] = response.xpath('//div[@class="tombstone-data-row" and ./strong[text()="CULTURE"]]//a/text()').get()
        item['date_description'] = " ".join(response.xpath('//div[@class="tombstone-data-row" and ./strong[text()="DATES"]]/text()').getall()).strip()
        item['maker_full_name'] = "|".join(response.xpath('//div[@class="tombstone-data-row" and ./strong[text()="ARTIST" or text()="MANUFACTURER"]]/a/text()').getall())
        item['accession_number'] = " ".join(response.xpath('//div[@class="tombstone-data-row" and ./strong[text()="ACCESSION NUMBER"]]/text()').getall()).strip()
        item['credit_line'] = " ".join(response.xpath('//div[@class="tombstone-data-row" and ./strong[text()="CREDIT LINE"]]/text()').getall()).strip()
        item['image_url'] = response.xpath('//div[contains(@class, "highlighted-image")]/img/@src').get()
        item['source_1'] = response.url

        yield item
