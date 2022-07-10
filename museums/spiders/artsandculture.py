import scrapy

import js2xml

from urllib.parse import urljoin, urlencode, parse_qsl

class ArtsAndCultureSpider(scrapy.Spider):
    name = 'artsandculture'
    allowed_domains = ['artsandculture.google.com']
    start_urls = ['https://artsandculture.google.com/search/partner']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_partners_html_page)

    def parse_partners_html_page(self, response):
        js = response.xpath('//script[contains(text(), "INIT_data")]/text()').get()
        parsed = js2xml.parse(js)
        links = parsed.xpath('//string[starts-with(text(), "/partner/")]/text()')

        for l in links:
            stub = stub = l.split('/')[-1]

            params = {
                'p': stub
            }

            url = 'https://artsandculture.google.com/search/asset/?' + urlencode(params)
            yield scrapy.Request(url, callback=self.parse_asset_search_html_page)

    def parse_partners_api_response(self, response):
        pass

    def parse_asset_search_html_page(self, response):
        js = response.xpath('//script[contains(text(), "INIT_data")]/text()').get()
        parsed = js2xml.parse(js)
        asset_links = parsed.xpath('//string[starts-with(text(), "/asset")]/text()')
        
        for al in asset_links:
            yield response.follow(al, callback=self.parse_asset_html_page)

        search_links = parsed.xpath('//string[starts-with(text(), "/search/asset")]/text()')
        
        for sl in search_links:
            yield response.follow(sl, callback=self.parse_asset_search_html_page)

    def parse_asset_search_api_response(self, response):
        pass

    def parse_asset_html_page(self, response):
        pass

