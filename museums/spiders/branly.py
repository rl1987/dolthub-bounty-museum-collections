import scrapy
from scrapy.selector import Selector

import json
from urllib.parse import urlparse, parse_qsl, urlencode

class BranlySpider(scrapy.Spider):
    name = 'branly'
    allowed_domains = ['www.quaibranly.fr']
    start_urls = ['https://www.quaibranly.fr/fr/explorer-les-collections/base/Work/action/list/?format=json&search=true&category=oeuvres&page=1&mode=thumb&orderby=null&order=desc&category=oeuvres&tx_mqbcollection_explorer%5Bquery%5D%5Btype%5D=&tx_mqbcollection_explorer%5Bquery%5D%5Bclassification%5D=&tx_mqbcollection_explorer%5Bquery%5D%5Bexemplaire%5D=']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)
        html_str = json_dict.get("html")

        sel = Selector(text=html_str)

        for link in sel.xpath('//a[@data-entity-type="Work"]/@href').getall():
            yield response.follow(link, callback=self.parse_object_page)

        total_pages = json_dict.get("nbPages")

        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))

        params = dict(old_params)
        page = int(params['page'])

        if page <= total_pages:
            page += 1
            params['page'] = page

            next_page_url = 'https://www.quaibranly.fr/fr/explorer-les-collections/base/Work/action/list/?' + urlencode(params)
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        pass

