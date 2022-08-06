import scrapy

from museums.items import ObjectItem


class BurkeSpider(scrapy.Spider):
    name = "burke"
    allowed_domains = ["www.burkemuseum.org"]
    start_urls = [
        "https://www.burkemuseum.org/collections-and-research/culture/contemporary-culture/database/browse.php"
    ]

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0], callback=self.parse_art_collection_page
        )

    def parse_art_collection_page(self, response):
        for l in response.xpath('//td[@class="collectionsText"]/a/@href').getall():
            yield response.follow(l, callback=self.parse_art_collection_page)

        for l in response.xpath('//td[@class="resultsData"]/a/@href').getall():
            yield response.follow(l, callback=self.parse_artwork_page)

    def parse_artwork_page(self, response):
        item = ObjectItem()

        item["object_number"] = response.xpath(
            '//tr[./td[text()="Object #"]]/td[@class="resultsData"]/text()'
        ).get()
        item["institution_name"] = "Burke Museum of Natural History and Culture"
        item["institution_city"] = "Seattle"
        item["institution_state"] = "WA"
        item["institution_country"] = "United States of America"
        item["institution_latitude"] = 47.660438537597656
        item["institution_longitude"] = -122.31153869628906
        item["department"] = response.xpath(
            '//ol[contains(@class, "breadcrumbs")]/li[.//a][last()]//a/text()'
        ).get()
        # XXX: category
        item["title"] = response.xpath(
            '//tr[./td[text()="Object name"]]/td[@class="resultsData"]/text()'
        ).get()
        # XXX: description, current_location
        item["dimensions"] = response.xpath(
            '//tr[./td[text()="Dimensions"]]/td[@class="resultsData"]/text()'
        ).get()
        # XXX: inscription, provenance
        item["materials"] = response.xpath(
            '//tr[./td[text()="Materials"]]/td[@class="resultsData"]/text()'
        ).get()
        item["technique"] = response.xpath(
            '//tr[./td[text()="Techniques"]]/td[@class="resultsData"]/text()'
        ).get()
        # XXX: from_location
        item["culture"] = response.xpath(
            '//tr[./td[text()="Culture of Origin"]]/td[@class="resultsData"]/text()'
        ).get()
        # XXX: date_description
        item["maker_full_name"] = response.xpath(
            '//tr[./td[text()="Maker or Artist"]]/td[@class="resultsData"]/text()'
        ).get()
        item["acquired_from"] = response.xpath(
            '//tr[./td[text()="Source"]]/td[@class="resultsData"]/text()'
        ).get()
        item["credit_line"] = response.xpath(
            '//tr[./td[text()="Credit"]]/td[@class="resultsData"]/text()'
        ).get()
        item["image_url"] = response.xpath(
            '//meta[@property="og:image"]/@content'
        ).get()
        item["source_1"] = response.url

        yield item
