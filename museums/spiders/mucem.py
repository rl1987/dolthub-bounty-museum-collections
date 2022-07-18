import scrapy
from scrapy.selector import Selector

import json
from urllib.parse import urlparse, urlencode, parse_qsl

from museums.items import ObjectItem

class MucemSpider(scrapy.Spider):
    name = 'mucem'
    allowed_domains = ['www.mucem.org']
    start_urls = ['https://www.mucem.org/en/collections/explorez-les-collections/next-page?term=a&page=1']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)
        html_str = json_dict.get("html")

        sel = Selector(text=html_str)

        for url in sel.xpath('//a/@href').getall():
            yield scrapy.Request(url, callback=self.parse_object_page)

        is_next_page = json_dict.get("next_button", False)
        if is_next_page:
            o = urlparse(response.url)
            params = dict(parse_qsl(o.query))
            params['page'] = int(params['page']) + 1

            next_page_url = 'https://www.mucem.org/en/collections/explorez-les-collections/next-page?' + urlencode(params)

            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        pass
