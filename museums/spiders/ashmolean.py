import scrapy

from museums.items import ObjectItem

class AshmoleanSpider(scrapy.Spider):
    name = 'ashmolean'
    allowed_domains = ['collections.ashmolean.org']
    start_urls = ['https://collections.ashmolean.org/collection/browse-9148']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        for url in response.xpath('//ul[@class="vr-list"]/li/a/@href').getall():
            yield scrapy.Request(url, callback=self.parse_object_page)

        next_page_url = response.xpath('//a[@class="next-btn"]/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        item = ObjectItem()

        item['source_1'] = response.xpath('//input[@id="ref-url"]/@value').get()

        item['object_number'] = item['source_1'].split('/')[-1]
        item['institution_name'] = 'Ashmolean Museum'
        item['institution_city'] = 'Oxford'
        item['institution_state'] = 'England'
        item['institution_country'] = 'United Kingdom'
        item['institution_latitude'] = 51.755332
        item['institution_longitude'] = -1.2611322
        item['department'] = response.xpath('//li[./div/p[text()="Museum department"]]/div[@class="right-wrap"]//p/text()').get("").strip()
        item['category'] = response.xpath('//li[./div/p[text()="Object type"]]/div[@class="right-wrap"]//a/text()').get("").strip()
        item['title'] = " ".join(response.xpath('//h1/text()').getall())
        item['description'] = " ".join(response.xpath('//div[@class="item-descrption"]/div/p/text()').getall())
        item['current_location'] = response.xpath('//li[./div/p[text()="Museum location"]]/div[@class="right-wrap"]//a/text()').get("").strip()
        item['dimensions'] = response.xpath('//li[./div/p[text()="Dimensions"]]/div[@class="right-wrap"]/div/text()').get("").strip()
        item['materials'] = response.xpath('//li[./div/p[text()="Material and technique"]]/div[@class="right-wrap"]/div/p/text()').get("").strip()
        item['from_location'] = "|".join(response.xpath('//li[./div/p[text()="Associated place"]]/div[@class="right-wrap"]//a/text()').getall())
        item['date_description'] = response.xpath('//li[./div/p[text()="Date"]]/div[@class="right-wrap"]/text()').get("").strip()
        item['maker_full_name'] = response.xpath('//li[./div/p[text()="Artist/maker"]]/div[@class="right-wrap"]//a/text()').get("").strip()
        item['accession_number'] = response.xpath('//li[./div/p[text()="Accession no."]]/div[@class="right-wrap"]/div/p/text()').get("").strip()
        item['credit_line'] = response.xpath('//li[./div/p[text()="Credit line"]]/div[@class="right-wrap"]/div/p/text()').get("").strip()
        item['image_url'] = response.xpath('//div[@class="firstimg"]/a/@href').get()

        yield item
