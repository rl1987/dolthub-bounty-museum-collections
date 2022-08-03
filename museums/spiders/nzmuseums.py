import scrapy

from museums.items import ObjectItem


class NzmuseumsSpider(scrapy.Spider):
    name = "nzmuseums"
    allowed_domains = ["www.nzmuseums.co.nz"]
    start_urls = ["https://www.nzmuseums.co.nz/objects?view=lightbox"]

    coords = dict()

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        for artwork_link in response.xpath(
            '//div[@class="lightbox-object-desc " or contains(@class, "lightbox-item-no-image")]/a/@href'
        ):
            yield response.follow(artwork_link, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[@aria-label="Next"]/@href').get()
        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse_search_page)

    def parse_object_page(self, response):
        self.logger.debug(response.meta)

        item = ObjectItem()

        item["object_number"] = (
            response.xpath('//p[contains(@class, "object_number")]/text()')
            .get("")
            .strip()
        )

        item["institution_name"] = response.xpath(
            '//div[@class="card"]/div[@class="card-body"]/a/text()'
        ).get()

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

        inscriptions = response.xpath(
            '//p[contains(@class, "inscription")]/text()'
        ).getall()
        inscriptions = list(map(lambda i: i.strip(), inscriptions))
        item["inscription"] = " ".join(inscriptions)

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
            '//div[@class="eh-carousel-centered-container" or @class="eh-object-detail-image-container"]/a/@href'
        ).get()
        item["source_1"] = response.url

        museum_coords = self.coords.get(item["institution_name"])
        if museum_coords is not None:
            item["institution_latitude"] = museum_coords.get("latitude")
            item["institution_longitude"] = museum_coords.get("longitude")
            yield item
        else:
            museum_link = response.xpath(
                '//div[@class="card"]/div[@class="card-body"]/a/@href'
            ).get()
            yield response.follow(
                museum_link, callback=self.parse_museum_coords, meta={"item": item}
            )

    def parse_museum_coords(self, response):
        item = response.meta.get("item")

        institution_latitude = response.xpath('//span[@id="latitude"]/text()').get()
        institution_longitude = response.xpath('//span[@id="longitude"]/text()').get()

        self.coords[item["institution_name"]] = {
            "latitude": institution_latitude,
            "longitude": institution_longitude,
        }

        item["institution_latitude"] = institution_latitude
        item["institution_longitude"] = institution_longitude

        yield item
