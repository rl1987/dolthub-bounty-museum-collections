import scrapy

from museums.items import ObjectItem


class BranlySpider(scrapy.Spider):
    name = "branly"
    allowed_domains = ["www.quaibranly.fr"]
    start_urls = [
        "https://www.quaibranly.fr/en/explore-collections/base/Work/action/show/notice/"
        + str(i)
        for i in range(1, 10000000)
    ]

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, callback=self.parse_object_page)

    def parse_object_page(self, response):
        item = ObjectItem()

        item["object_number"] = "".join(
            response.xpath(
                '//li[@class="description-item" and ./b[text()="Numéro de gestion :"]]/text()'
            ).getall()
        ).strip()
        item["institution_name"] = "Musée du quai Branly"
        item["institution_city"] = "Paris"
        item["institution_state"] = "Île-de-France"
        item["institution_country"] = "France"
        item["institution_latitude"] = 48.8609242
        item["institution_longitude"] = 2.2968265
        # XXX: department
        item["category"] = " ".join(
            response.xpath(
                '//li[@class="description-item" and ./b[text()="Type d\'objet :"]]/text()'
            ).getall()
        ).strip()
        item["title"] = response.xpath('//div[@class="intro"]/h1/text()').get()
        item["description"] = (
            response.xpath('//div[@class="edito"]/p[@class="more"]/text()')
            .get("")
            .strip()
        )
        item["current_location"] = " ".join(
            response.xpath(
                '//li[@class="description-item" and ./b[text()="Exposé :"]]/text()'
            ).getall()
        ).strip()
        item["dimensions"] = " ".join(
            response.xpath(
                '//li[@class="description-item" and ./b[text()="Dimensions et poids :"]]/text()'
            ).getall()
        ).strip()
        # XXX: inscription, provenance
        item["materials"] = " ".join(
            response.xpath(
                '//li[@class="description-item" and ./b[text()="Matériaux et techniques :"]]/text()'
            ).getall()
        ).strip()
        from_locations = response.xpath('//li[@class="description-item" and ./b[text()="Géographie : "]]/a/text()').getall()
        from_locations = list(map(lambda fl: fl.strip(), from_locations))
        from_locations = "|".join(from_locations)
        item['from_location'] = from_locations
        cultures = response.xpath(
            '//li[@class="description-item" and ./b[text()="Culture : "]]/a/text()'
        ).getall()
        cultures = list(map(lambda c: c.strip(), cultures))
        cultures = "|".join(cultures)
        item["culture"] = cultures
        item["date_description"] = " ".join(
            response.xpath(
                '//li[@class="description-item" and ./b[text()="Date :"]]/text()'
            ).getall()
        ).strip()
        item["maker_full_name"] = (
            response.xpath(
                '//li[@class="description-item" and ./b[text()="Photographe : " or text()="Dessinateur : "]]/a/text()'
            )
            .get("")
            .strip()
        )  # XXX: improve to cover more types of makers
        # XXX: maker_role
        item["acquired_from"] = (
            response.xpath(
                '//li[@class="description-item" and ./b[text()="Donateur : "]]/a/text()'
            )
            .get("")
            .strip()
        )
        item["accession_number"] = "".join(
            response.xpath(
                '//li[@class="description-item" and ./b[text()="Numéro d\'inventaire :"]]/text()'
            ).getall()
        ).strip()
        item["image_url"] = response.xpath("//li/@data-zoom").get()
        item["source_1"] = response.url

        if item["object_number"] == "":
            item["object_number"] = item["accession_number"]

        yield item
