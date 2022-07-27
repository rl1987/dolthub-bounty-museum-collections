import scrapy

from urllib.parse import urljoin

from museums.items import ObjectItem

THRESHOLD = 25


class EhiveSpider(scrapy.Spider):
    name = "ehive"
    allowed_domains = ["ehive.com"]
    start_urls = ["https://ehive.com/collections"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_collection_list)

    def parse_collection_list(self, response):
        for museum_link in response.xpath(
            '//a[@class="eh-summary-account-record-profile-name"]/@href'
        ).getall():
            museum_url = urljoin(response.url, museum_link)
            yield scrapy.Request(museum_url, callback=self.parse_museum_page)

        next_page_link = response.xpath('//a[@aria-label="Next"]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_collection_list)

    def parse_museum_page(self, response):
        institution_name = (
            response.xpath("//title/text()").get().replace(" on eHive", "")
        )
        institution_latitude = response.xpath('//span[@id="latitude"]/text()').get()
        institution_longitude = response.xpath('//span[@id="longitude"]/text()').get()

        if not "Museum" in institution_name:
            if (
                "Archive" in institution_name
                or "School" in institution_name
                or "Park" in institution_name
                or "Cathedral" in institution_name
            ):
                return

        meta = {
            "institution_name": institution_name,
            "institution_latitude": institution_latitude,
            "institution_longitude": institution_longitude,
        }

        view_all_text = response.xpath(
            '//h5[text()="Entire collection - "]/a/text()'
        ).get()
        n = view_all_text.replace("View all (", "").replace(")", "")
        n = int(n)
        if n < THRESHOLD:
            return

        # TODO: come up with a way to remove data from what appears to be test profiles
        view_all_link = response.xpath(
            '//h5[text()="Entire collection - "]/a/@href'
        ).get()
        view_all_url = urljoin(response.url, view_all_link)
        yield scrapy.Request(view_all_url, callback=self.parse_object_list, meta=meta)

    def parse_object_list(self, response):
        meta = {
            "institution_name": response.meta.get("institution_name"),
            "institution_latitude": response.meta.get("institution_latitude"),
            "institution_longitude": response.meta.get("institution_longitude"),
        }

        for object_link in response.xpath('//p[@class="title"]/a/@href').getall():
            object_url = urljoin(response.url, object_link)
            yield scrapy.Request(object_url, callback=self.parse_object_page, meta=meta)

        next_page_link = response.xpath('//a[@aria-label="Next"]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(
                next_page_url, callback=self.parse_object_list, meta=meta
            )

    def parse_object_page(self, response):
        self.logger.debug(response.meta)

        item = ObjectItem()

        item["object_number"] = (
            response.xpath('//p[contains(@class, "object_number")]/text()')
            .get("")
            .strip()
        )

        item["institution_name"] = response.meta.get("institution_name")
        item["institution_latitude"] = response.meta.get("institution_latitude")
        item["institution_longitude"] = response.meta.get("institution_longitude")

        item["category"] = (
            response.xpath('//p[contains(@class, "object_type")]/a/text()')
            .get("")
            .strip()
        )
        item["department"] = (
            response.xpath('//p[contains(@class, "named_collection")]/text()')
            .get("")
            .strip()
        )
        item["title"] = (
            response.xpath('//p[contains(@class, "name")]/text()').get("").strip()
        )
        item["description"] = response.xpath(
            '//p[contains(@class, "web_public_description")]/text()'
        ).getall()
        item["description"] = list(map(lambda d: d.strip(), item["description"]))
        item["description"] = " ".join(item["description"])

        item["dimensions"] = (
            response.xpath('//p[contains(@class, "measurement_description")]/text()')
            .get("")
            .strip()
        )
        item["inscription"] = (
            response.xpath('//p[contains(@class, "inscription")]/text()')
            .get("")
            .strip()
        )
        item["materials"] = response.xpath(
            '//p[contains(@class, "medium_description")]/text()'
        ).getall()
        item["materials"] = list(map(lambda m: m.strip(), item["materials"]))
        item["materials"] = " ".join(item["materials"])
        item["from_location"] = (
            response.xpath('//p[contains(@class, "place_made")]/a/text()')
            .get("")
            .strip()
        )
        item["date_description"] = (
            response.xpath('//p[contains(@class, "date_made")]/text()').get("").strip()
        )
        item["maker_full_name"] = response.xpath(
            '//p[contains(@class, "primary_creator_maker")]/a/text()'
        ).getall()
        # Fuck this is getting repetitive...
        item["maker_full_name"] = list(
            map(lambda m: m.strip(), item["maker_full_name"])
        )
        item["maker_full_name"] = "|".join(item["maker_full_name"])
        item["maker_role"] = response.xpath(
            '//p[contains(@class, "primary_creator_maker_role")]/text()'
        ).getall()
        item["maker_role"] = list(map(lambda m: m.strip(), item["maker_role"]))
        item["maker_role"] = "|".join(item["maker_role"])

        item["credit_line"] = (
            response.xpath('//p[contains(@class, "credit_line")]/text()')
            .get("")
            .strip()
        )
        item["image_url"] = response.xpath(
            '//a[./img[@class="eh-low-res-image"]]/@href'
        ).get()
        item["source_1"] = response.url

        yield item
