import scrapy

import string
from urllib.parse import urlencode, urljoin

PER_PAGE = 100


class AucklandSpider(scrapy.Spider):
    name = "auckland"
    allowed_domains = ["aucklandmuseum.com"]
    start_urls = ["https://www.aucklandmuseum.com/discover/collections-online/search"]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        categories = [
            "ecrm:E22_Man-Made_Object",
            "ecrm:E84_Information_Carrier",
            "ecrm:E20_Biological_Object",
            "am_isTaonga",
        ]
        departments = [
            "Applied Arts and Design",
            "Archaeology",
            "Botany",
            "Entomology",
            "Ethnology",
            "Geology",
            "History",
            "Maori",
            "Marine",
            "Māori",
            "Pacific",
            "Pictorial",
            "World",
            "[library]",
            "birds",
            "botany",
            "ephemera",
            "land mammals",
            "manuscripts and archives",
            "painting and drawings",
            "photography",
            "publication",
            "reptiles and amphibians",
        ]

        search_url = "https://www.aucklandmuseum.com/discover/collections-online/search"

        for letter in string.ascii_lowercase:
            for c in categories:
                for d in departments:
                    params = {"c": c, "dept": d, "k": letter, "pp": PER_PAGE}

                    url = search_url + "?" + urlencode(params)

                    yield scrapy.Request(url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        object_links = response.xpath(
            '//a[.//figure[contains(@class, "search-results--thumbnail")]]/@href'
        ).getall()

        for object_link in object_links:
            object_link = object_link.split("?")[0]
            object_url = urljoin(response.url, object_link)
            yield scrapy.Request(object_url, callback=self.parse_object_page)

        next_page_link = response.xpath(
            '//div[contains(@class, "next-results")]/a/@href'
        ).get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        pass
