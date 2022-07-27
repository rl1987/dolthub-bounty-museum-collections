import scrapy

from museums.items import ObjectItem


class NgscottlandSpider(scrapy.Spider):
    name = "ngscottland"
    allowed_domains = ["nationalgalleries.org"]
    start_urls = ["https://www.nationalgalleries.org/search?sort=title&page=0"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        links = response.xpath(
            '//h2/a[contains(@class, "ngs-search-result__link")]/@href'
        ).getall()
        for l in links:
            yield response.follow(l, callback=self.parse_artwork_page)

        next_page_link = response.xpath(
            '//a[contains(@class, "ngs-pagination__link--next")]/@href'
        ).get()
        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse_search_page)

    def parse_artwork_page(self, response):
        item = ObjectItem()

        item["object_number"] = response.url.split("?")[0].split("/")[-1]
        item["institution_name"] = "National Galleries Scotland"
        item["institution_city"] = "Edinburgh"
        item["institution_state"] = "Scotland"
        item["institution_country"] = "United Kingdom"
        item["institution_latitude"] = 55.9507549
        item["institution_longitude"] = -3.2266089
        item["category"] = response.xpath(
            '//a[@data-ngs-type="object-type"]/text()'
        ).get()
        item["title"] = (
            response.xpath('//h1[contains(@class, "ngs-title-block__title")]/text()')
            .get("")
            .strip()
        )
        item["description"] = " ".join(
            response.xpath(
                '//div[@class="ngs-artwork-about__content"]/div/p//text()'
            ).getall()
        )
        item["current_location"] = "|".join(
            response.xpath(
                '//li[@class="ngs-mimsy-data__item"]//a[contains(@href, "/search?location")]/text()'
            ).getall()
        )
        item["dimensions"] = (
            response.xpath(
                '//li[@class="ngs-mimsy-data__item" and ./div[text()="measurements:"]]/div[@class="ngs-mimsy-data__item-values"]/text()'
            )
            .get("")
            .strip()
        )
        item["materials"] = "|".join(
            response.xpath(
                '//li[@class="ngs-mimsy-data__item" and ./div[text()="materials:"]]/div[@class="ngs-mimsy-data__item-values"]/div//text()'
            ).getall()
        )
        item["culture"] = "|".join(
            response.xpath('//a[@ngs-data-type="nationality"]/text()').getall()
        )
        item["date_description"] = (
            response.xpath(
                '//li[@class="ngs-mimsy-data__item" and ./div[text()="date created:"]]/div[@class="ngs-mimsy-data__item-values"]/text()'
            )
            .get("")
            .strip()
        )
        item["maker_full_name"] = "|".join(
            response.xpath('//a[@data-ngs-type="artist"]/text()').getall()
        )
        item["accession_number"] = (
            response.xpath(
                '//li[@class="ngs-mimsy-data__item" and ./div[text()="accession number:"]]/div[@class="ngs-mimsy-data__item-values"]/div/text()'
            )
            .get("")
            .strip()
        )
        item["credit_line"] = (
            response.xpath(
                '//li[@class="ngs-mimsy-data__item" and ./div[text()="credit line:"]]/div[@class="ngs-mimsy-data__item-values"]/text()'
            )
            .get("")
            .strip()
        )
        item["image_url"] = response.xpath('//meta[@itemprop="image"]/@content').get()
        item["source_1"] = response.url

        yield item
