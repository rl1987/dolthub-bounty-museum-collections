import scrapy

from urllib.parse import urlencode, urlparse, parse_qsl

PER_PAGE = 48

from museums.items import ObjectItem


class DigitaltmuseumSpider(scrapy.Spider):
    name = "digitaltmuseum"
    allowed_domains = ["digitaltmuseum.org"]
    start_urls = ["https://digitaltmuseum.org/owners/"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_owner_list)

    def parse_owner_list(self, response):
        for l in response.xpath('//a[@class="module__grid"]/@href').getall():
            yield response.follow(l, callback=self.parse_owner_page)

    def parse_owner_page(self, response):
        latitude = response.xpath('//figure[@class="c-owner-map"]/@lat').get()
        longitude = response.xpath('//figure[@class="c-owner-map"]/@lng').get()

        meta_dict = {
            "latitude": latitude,
            "longitude": longitude,
        }

        owner_abbrev = response.url.split("/")[-1]

        search_link = "https://digitaltmuseum.org/search/?aq=owner%3A%22{}%22".format(
            owner_abbrev
        )
        yield response.follow(
            search_link, callback=self.parse_search_page, meta=meta_dict
        )

    def parse_search_page(self, response):
        meta_dict = {
            "latitude": response.meta.get("latitude"),
            "longitude": response.meta.get("longitude"),
        }

        got_results = 0

        for l in response.xpath('//a[@class="module__grid"]/@href').getall():
            if l.startswith("/owner") or l.startswith("/search"):
                continue

            got_results += 1
            yield response.follow(l, callback=self.parse_object_page, meta=meta_dict)

        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))

        params = dict(old_params)

        if old_params.get("o") is None:
            params["o"] = got_results
            params["n"] = PER_PAGE
            params["omit"] = 1
        else:
            if got_results < PER_PAGE:
                return

            params["o"] = int(old_params["o"]) + PER_PAGE

        next_page_url = "https://digitaltmuseum.org/search/?" + urlencode(params)
        yield scrapy.Request(next_page_url, self.parse_search_page, meta=meta_dict)

    def parse_object_page(self, response):
        item = ObjectItem()

        item["institution_name"] = response.xpath(
            '//li[./b[text()="Institution"]]/a/text()'
        ).get()
        item["institution_latitude"] = response.meta.get("latitude")
        item["institution_longitude"] = response.meta.get("longitude")
        item["department"] = "".join(
            response.xpath('//li[./b[text()="Part of collection"]]/text()').getall()
        ).strip()
        item["category"] = (
            response.xpath('//li[./b[text()="Type"]]/a/text()').get("").strip()
        )
        item["title"] = response.xpath('//div[@class="article__title"]/h1/text()').get()
        item["description"] = " ".join(
            response.xpath(
                '//div[@class="article__leadtext"]/div[@class="text__expanded"]/p/text()'
            ).getall()
        ).strip()
        item["dimensions"] = " ".join(
            response.xpath('//li[./b[text()="Dimensions"]]/text()').getall()
        ).strip()
        item["inscription"] = " ".join(
            response.xpath('//li[./b[text()="Inscription"]]/ul/li/text()').getall()
        ).strip()
        item["provenance"] = " ".join(
            response.xpath('//li[./b[text()="Provenance"]]/text()').getall()
        ).strip()
        item["materials"] = "|".join(
            response.xpath('//li[./b[text()="Materials"]]/a/text()').getall()
        ).strip()
        item["technique"] = "|".join(
            response.xpath('//li[./b[text()="Techniques"]]/a/text()').getall()
        ).strip()
        item["maker_full_name"] = "|".join(
            response.xpath('//li[./b[text()="Produsent"]]/a/text()').getall()
        )
        item["from_location"] = "|".join(
            response.xpath('//li[./b[text()="Place of creation"]]/a/text()').getall()
        )
        item["description"] = " ".join(
            response.xpath('//div[@class="article__leadtext"]/p/text()').getall()
        )
        item["date_description"] = " ".join(
            response.xpath('//li[./b[text()="Creation date"]]/text()').getall()
        ).strip()
        item["maker_full_name"] = "|".join(
            response.xpath('//li[./b[text()="Artist"]]/a/text()').getall()
        ).strip()
        item["acquired_from"] = " ".join(
            response.xpath('//li[./b[text()="Acquisition"]]/text()').getall()
        ).strip()
        item["image_url"] = response.xpath(
            '//meta[@property="og:image"]/@content'
        ).get()
        item["source_1"] = response.url
        try:
            item["object_number"] = (
                response.xpath('//li[./b[text()="Identifier"]]/text()')
                .getall()[-1]
                .strip()
            )
        except:
            item["object_number"] = response.url.split("/")[-2]

        yield item
