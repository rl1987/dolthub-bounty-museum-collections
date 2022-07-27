import scrapy

from urllib.parse import urlparse, urlencode, parse_qsl

from museums.items import ObjectItem


class ScienceSpider(scrapy.Spider):
    name = "science"
    allowed_domains = ["collection.sciencemuseumgroup.org.uk"]
    start_urls = [
        "https://collection.sciencemuseumgroup.org.uk/objects/co{}".format(i)
        for i in range(1, 1000000)
    ]  # HACK to bypass 1000 results limit

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, callback=self.parse_object_page)

    def parse_object_page(self, response):
        item = ObjectItem()

        item["object_number"] = response.url.split("/")[-1].replace("co", "")
        item["institution_name"] = "Science Museum Group"
        item["institution_country"] = "United Kingdom"
        item["department"] = (
            response.xpath('//dl[contains(@class, "details-Collection")]/dd/a/text()')
            .get("")
            .strip()
        )
        item["category"] = (
            response.xpath('//dl[contains(@class, "details-Category")]/dd/a/text()')
            .get("")
            .strip()
        )
        item["title"] = (
            response.xpath('//h1[@class="record-top__title"]/text()').get("").strip()
        )
        item["description"] = response.xpath(
            '//meta[@property="og:description"]/@content'
        ).get()
        item["current_location"] = response.xpath(
            '//div[./h2[contains(text(), "On display")]]/p/a/text()'
        ).get()
        item["dimensions"] = " ".join(
            response.xpath(
                '//dl[contains(@class, "details-Measurements")]/dd/text()'
            ).getall()
        ).strip()
        materials = response.xpath(
            '//dl[contains(@class, "details-Materials")]/dd/a/text()'
        ).getall()
        materials = list(map(lambda m: m.strip(), materials))
        materials = "|".join(materials)
        item["materials"] = materials
        item["from_location"] = (
            response.xpath('//dl[contains(@class, "fact-Made")]/dd/a[2]/text()')
            .get("")
            .strip()
        )
        item["date_description"] = (
            response.xpath('//dl[contains(@class, "fact-Made")]/dd/a[1]/text()')
            .get("")
            .strip()
        )
        makers = response.xpath(
            '//dl[contains(@class, "fact-maker")]/dd/a/text()'
        ).getall()
        makers = list(map(lambda m: m.strip(), makers))
        makers = "|".join(makers)
        item["maker_full_name"] = makers
        item["credit_line"] = (
            response.xpath('//dl[contains(@class, "details-credit")]/dd/text()')
            .get("")
            .strip()
        )
        item["accession_number"] = (
            response.xpath(
                '//dl[contains(@class, "details-Object-Number") or contains(@class, "details-Identifier")]/dd/text()'
            )
            .get("")
            .strip()
        )

        item["image_url"] = response.xpath(
            '//div[@class="carousel"]/img/@data-flickity-lazyload'
        ).get()
        item["source_1"] = response.url
        item["source_2"] = response.xpath(
            '//a[./abbr[@title="Javascript Object Notation"]]/@href'
        ).get()

        yield item
