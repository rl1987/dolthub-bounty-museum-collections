import scrapy

from urllib.parse import urljoin

from museums.items import ObjectItem

class SeamusemSpider(scrapy.Spider):
    name = 'seamusem'
    allowed_domains = ['sea.museum']
    start_urls = ['http://collections.sea.museum/search/*/objects?filter=MediaExistence%3Atrue#filters',
            'http://collections.sea.museum/search/*/objects?filter=MediaExistence%3Afalse']

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        for object_link in response.xpath('//a[starts-with(@href, "/objects/")]/@href').getall():
            object_link = object_link.split(";")[0]
            object_url = urljoin(response.url, object_link)
            yield scrapy.Request(object_url, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[contains(@class, "next-page-link")]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        item = ObjectItem()

        item['object_number'] = response.xpath('//div[contains(@class, "invnoField")]/span[@class="detailFieldValue"]/text()').get()
        item['institution_name'] = 'Australian National Maritime Museum'
        item['institution_city'] = 'Sydney'
        item['institution_state'] = 'NSW'
        item['institution_country'] = 'Australia'
        item['institution_latitude'] = -33.8693567
        item['institution_longitude'] = 151.1964441
        item['title'] = response.xpath('//div[contains(@class, "titleField")]/h1/text()').get()
        item['category'] = response.xpath('//div[contains(@class, "classificationField")]/span/a/text()').get()
        item['description'] = " ".join(response.xpath('//div[@class="descriptionText"]/text()').getall())
        item['dimensions'] = response.xpath('//div[contains(@class, "dimensionsField")]/span[@class="detailFieldValue"]/div/text()').get()
        item['materials'] = response.xpath('//div[contains(@class, "mediumField")]/span[@class="detailFieldValue"]/text()').get()
        item['from_location'] = response.xpath('//div[./span[text()="Place Manufactured:"]]/span[last()]/text()').get()
        item['date_description'] = response.xpath('//div[contains(@class, "displayDateField")]/span[@class="detailFieldValue"]/text()').get()
        item['maker_full_name'] = response.xpath('//div[contains(@class, "primaryMakerField")]/span/a/text()').get()
        item['credit_line'] = response.xpath('//div[contains(@class, "creditlineField")]/span[@class="detailFieldValue"]/text()').get()
        item['image_url'] = response.xpath('//img[@class="disable-click"]/@src').get()
        if item.get('image_url') is not None:
            item['image_url'] = urljoin(response.url, item['image_url'])
        item['source_1'] = response.url

        yield item
