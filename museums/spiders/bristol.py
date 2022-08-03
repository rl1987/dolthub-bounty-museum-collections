import scrapy

from museums.items import ObjectItem

from urllib.parse import urljoin


class BristolSpider(scrapy.Spider):
    name = "bristol"
    allowed_domains = ["museums.bristol.gov.uk"]
    start_urls = ["https://museums.bristol.gov.uk/list.php"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_object_list)

    def parse_object_list(self, response):
        for l in response.xpath('//div[@class="media"]//a/@href').getall():
            yield response.follow(l, callback=self.parse_object_page)

        next_page_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse_object_list)

    def parse_object_page(self, response):
        item = ObjectItem()

        item["object_number"] = response.xpath(
            '//p[./label[text()="Object Number"]]/text()'
        ).get()
        item["institution_name"] = "Bristol's Free Museums and Historic Houses"
        item["institution_city"] = "Bristol"
        item["institution_country"] = "United Kingdom"
        item["department"] = response.xpath(
            '//p[./label[text()="Collection"]]/text()'
        ).get()
        item["title"] = (
            response.xpath('//div[@class="page-header"]/h3/text()').get("").strip()
        )
        item["description"] = response.xpath(
            '//p[./label[text()="Description"]]/text()'
        ).get()
        item["current_location"] = " ".join(
            response.xpath('//div[./div/h3[text()="Current Location"]]/text()').getall()
        ).strip()
        item["maker_full_name"] = response.xpath(
            '//p[./label[text()="Artist"]]/text()'
        ).get()
        item["image_url"] = response.xpath('//img[@id="big-img"]/@src').get()
        if item["image_url"] is not None:
            item["image_url"] = urljoin(response.url, item["image_url"])

        if item["object_number"] is not None:
            item["object_number"] = item["object_number"][2:]

        if item["department"] is not None:
            item["department"] = item["department"][2:]

        if item["description"] is not None:
            item["description"] = item["description"][2:]

        if item["maker_full_name"] is not None:
            item["maker_full_name"] = item["maker_full_name"][2:]

        item["source_1"] = response.url

        yield item
