import scrapy

from urllib.parse import urljoin

from museums.items import ObjectItem

class EhiveSpider(scrapy.Spider):
    name = 'ehive'
    allowed_domains = ['ehive.com']
    start_urls = ['https://ehive.com/objects']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_object_list)

    def parse_object_list(self, response):
        for object_link in response.xpath('//a[./img[@class="eh-image"]]/@href').getall():
            object_url = urljoin(response.url, object_link)
            yield scrapy.Request(object_url, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[@aria-label="Next"]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_object_list)

    def parse_object_page(self, response):
        item = ObjectItem()
    
        item['object_number'] = response.xpath('//p[contains(@class, "object_number")]/text()').get("").strip()

        item['institution_name'] = response.xpath('//a[starts-with(@href, "/collections/")]/text()').get()

        item['category'] = response.xpath('//p[contains(@class, "object_type")]/a/text()').get("").strip()
        item['department'] = response.xpath('//p[contains(@class, "named_collection")]/text()').get("").strip()
        item['title'] = response.xpath('//p[contains(@class, "name")]/text()').get("").strip()
        item['description'] = response.xpath('//p[contains(@class, "web_public_description")]/text()').getall()
        item['description'] = list(map(lambda d: d.strip(), item['description']))
        item['description'] = " ".join(item['description'])
        
        item['dimensions'] = response.xpath('//p[contains(@class, "measurement_description")]/text()').get("").strip()
        item['inscription'] = response.xpath('//p[contains(@class, "inscription")]/text()').get("").strip()
        item['materials'] = response.xpath('//p[contains(@class, "medium_description")]/text()').getall()
        item['materials'] = list(map(lambda m: m.strip(), item['materials']))
        item['materials'] = " ".join(item['materials'])
        item['from_location'] = response.xpath('//p[contains(@class, "place_made")]/a/text()').get("").strip()
        item['date_description'] = response.xpath('//p[contains(@class, "date_made")]/text()').get("").strip()
        item['maker_full_name'] = response.xpath('//p[contains(@class, "primary_creator_maker")]/a/text()').getall()
        # Fuck this is getting repetitive...
        item['maker_full_name'] = list(map(lambda m: m.strip(), item['maker_full_name']))
        item['maker_full_name'] = "|".join(item['maker_full_name'])
        item['maker_role'] = response.xpath('//p[contains(@class, "primary_creator_maker_role")]/text()').getall()
        item['maker_role'] = list(map(lambda m: m.strip(), item['maker_role']))
        item['maker_role'] = "|".join(item['maker_role'])
        
        item['credit_line'] = response.xpath('//p[contains(@class, "credit_line")]/text()').get("").strip()
        item['image_url'] = response.xpath('//a[./img[@class="eh-low-res-image"]]/@href').get()
        item['source_1'] = response.url
        
        yield item

