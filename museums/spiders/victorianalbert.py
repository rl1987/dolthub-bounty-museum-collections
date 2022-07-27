import scrapy

import json
from urllib.parse import urlparse, urlencode, parse_qsl

from museums.items import ObjectItem

# https://collections.vam.ac.uk/search/?page=1&page_size=15


class VictoriaNAlbertSpider(scrapy.Spider):
    name = "victorianalbert"
    allowed_domains = ["api.vam.ac.uk", "collections.vam.ac.uk"]
    start_urls = [
        "https://collections.vam.ac.uk/item/O" + str(i) for i in range(1, 2000000)
    ]

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, callback=self.parse_object_page)

    def parse_object_page(self, response):
        item = ObjectItem()

        item["object_number"] = (
            response.xpath('//meta[@property="og:url"]/@content')
            .get()
            .replace("/item/", "")
            .replace("/", "")
        )
        item["institution_name"] = "Victoria and Albert Museum"
        item["institution_city"] = "London"
        item["institution_state"] = "England"
        item["institution_country"] = "United Kingdom"
        item["institution_latitude"] = 51.494720458984375
        item["institution_longitude"] = -0.1917800009250641
        item["category"] = response.xpath(
            '//a[@data-tracking-collections="tag - category"]/div/text()'
        ).get()
        item["title"] = response.xpath('//h1[@class="object-page__title"]/text()').get()
        # XXX: current_location
        item["dimensions"] = "|".join(
            response.xpath('//tr[./td[text()="Dimensions"]]//li/text()').getall()
        )
        item["inscription"] = "|".join(
            response.xpath(
                '//tr[./td[text()="Marks and Inscriptions"]]//li/text()'
            ).getall()
        )
        item["provenance"] = response.xpath(
            '//tr[./td[text()="Object history"]]//div[@class="etc-details__cell-free-content"]/text()'
        ).get()
        item["technique"] = "|".join(
            response.xpath(
                '//a[@data-tracking-collections="tag - material"]/div/text()'
            ).getall()
        )
        item["from_location"] = "|".join(
            response.xpath(
                '//a[@data-tracking-collections="tag - place"]/div/text()'
            ).getall()
        )
        # XXX: date_description, year_start, year end

        makers = response.xpath(
            '//tr[./td[text()="Artist/Maker"]]//div[@class="etc-details__controlled-vocab-content"]/text()'
        ).getall()

        maker_names = []
        maker_roles = []

        for m in makers:
            maker_names.append(m.split(" (")[0])
            maker_roles.append(m.split(" (")[-1].replace(")", ""))

        item["maker_full_name"] = "|".join(maker_names)
        item["maker_role"] = "|".join(maker_roles)
        item["accession_number"] = response.xpath(
            '//tr[./td[text()="Accession Number"]]//div/text()'
        ).get()
        item["credit_line"] = response.xpath(
            '//tr[./td[text()="Credit line"]]//div/text()'
        ).get()
        item["image_url"] = response.xpath(
            '//img[@class="object-page__hero-img"]/@src'
        ).get()
        item["source_1"] = response.url

        yield item
