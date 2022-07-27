import scrapy

from urllib.parse import urljoin

from museums.items import ObjectItem


class MnhnFrSpider(scrapy.Spider):
    name = "mnhn_fr"
    allowed_domains = ["science.mnhn.fr"]
    start_urls = ["https://science.mnhn.fr/institution/mnhn/item/list?startIndex=0"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        item_links = response.xpath('//div[@class="title"]/a/@href').getall()

        for item_link in item_links:
            url = urljoin(response.url, item_link)
            yield scrapy.Request(url, callback=self.parse_item_page)

        next_page_link = response.xpath(
            '//a[./i[@class="icon-arrow-right"]]/@href'
        ).get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_item_page(self, response):
        item = ObjectItem()

        item["object_number"] = response.xpath(
            '//div[@class="catalog-number-marked"]/text()'
        ).get()
        item["institution_name"] = "Muséum national d'Histoire naturelle"
        item["institution_city"] = "Paris"
        item["institution_state"] = "Île-de-France"
        item["institution_country"] = "France"
        item["institution_latitude"] = 48.8434
        item["institution_longitude"] = 2.3635
        item["department"] = response.xpath(
            '//div[@itemprop="department"]/div/text()'
        ).get()
        item["category"] = response.xpath(
            '//label[@for="catalog-number"]/span/text()'
        ).get()
        item["title"] = response.xpath("//title/text()").get()
        item["description"] = (
            response.xpath('//div[@id="noteDesc"]/text()').get("").strip()
        )
        item["dimensions"] = response.xpath('//div[@id="size"]/text()').get("").strip()
        # XXX: current_location
        # XXX: provenance
        item["acquired_from"] = (
            response.xpath('//div[@id="recordedBy"]/a/text()').get("").strip()
        )
        item["from_location"] = (
            response.xpath('//div[@id="country"]/a/text()').get("").strip()
        )
        item["date_description"] = (
            response.xpath('//div[@id="eventDate"]/text()').get("").strip()
        )
        item["image_url"] = response.xpath('//div[@class="media-image"]/img/@src').get()
        item["source_1"] = response.url

        yield item
