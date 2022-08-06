import scrapy

from museums.items import ObjectItem


class IndianaSpider(scrapy.Spider):
    name = "indiana"
    allowed_domains = ["collection.indianamuseum.org"]
    start_urls = [
        "https://collection.indianamuseum.org/mwebcgi/mweb.exe?request=record;id={};type=101".format(
            i
        )
        for i in range(1, 1000000)
    ]

    def parse(self, response):
        if "Record not found" in response.text:
            return

        item = ObjectItem()

        item["object_number"] = response.xpath(
            '//dt[text()="ID Number"]/following-sibling::dd/text()'
        ).get()
        item["institution_name"] = "Indiana state museum and historic sites"
        item["institution_city"] = "Indianapolis"
        item["institution_state"] = "IN"
        item["institution_country"] = "United States of America"
        item["institution_latitude"] = 39.7683919
        item["institution_longitude"] = -86.1695013
        # XXX: department, category
        item["title"] = response.xpath(
            '//dt[text()="Title"]/following-sibling::dd/text()'
        ).get()
        item["description"] = " ".join(
            response.xpath(
                '//dt[text()="Description"]/following-sibling::dd/p/text()'
            ).getall()
        )
        # XXX: current_location, inscription, provenance
        item["dimensions"] = response.xpath(
            '//dt[text()="Measurements"]/following-sibling::dd/text()'
        ).get()
        item["materials"] = response.xpath(
            '//dt[text()="Materials"]/following-sibling::dd/text()'
        ).get()
        # XXX: technique
        item["from_location"] = response.xpath(
            '//dt[text()="Place"]/following-sibling::dd/text()'
        ).get()
        # XXX: culture
        item["date_description"] = response.xpath(
            '//dt[text()="Year"]/following-sibling::dd/text()'
        ).get()
        item["maker_full_name"] = "|".join(
            response.xpath(
                '//dt[text()="Maker"]/following-sibling::dd//a/text()'
            ).getall()
        )
        # XXX: acquired, accession...
        item["credit_line"] = response.xpath(
            '//dt[text()="Credit Line"]/following-sibling::dd/text()'
        ).get()
        item["image_url"] = response.xpath(
            '//div[@class="fullRecImage"]//img/@src'
        ).get()
        item["source_1"] = response.url

        yield item
