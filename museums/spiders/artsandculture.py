import scrapy

import js2xml

import json
from urllib.parse import urlparse, urlencode, parse_qsl

class ArtsAndCultureSpider(scrapy.Spider):
    name = 'artsandculture'
    allowed_domains = ['artsandculture.google.com']
    start_urls = ['https://artsandculture.google.com/search/partner']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_partners_html_page)

    def partner_asset_search_request_from_link(self, l):
        stub = stub = l.split('/')[-1]

        params = {
            'p': stub
        }

        url = 'https://artsandculture.google.com/search/asset/?' + urlencode(params)
        return scrapy.Request(url, callback=self.parse_asset_search_html_page)

    def partner_api_request_from_pt(self, pt):
        params = {
            's': 24,
            'pt': pt,
            'hl': 'en',
            'rt': 'j'
        }

        url = 'https://artsandculture.google.com/api/objects/partner?' + urlencode(params)
        return scrapy.Request(url, callback=self.parse_partners_api_response)

    def parse_partners_html_page(self, response):
        js = response.xpath('//script[contains(text(), "INIT_data")]/text()').get()
        parsed = js2xml.parse(js)
        links = parsed.xpath('//string[starts-with(text(), "/partner/")]/text()')

        for l in links:
            yield self.partner_asset_search_request_from_link(l)

        try:
            pt = parsed.xpath('//right/array/array/string[last()]/text()')[0]
        except:
            return

        yield self.partner_api_request_from_pt(pt)

    def parse_partners_api_response(self, response):
        json_str = response.text
        json_str = json_str[5:]

        json_arr = json.loads(json_str)
        
        try:
            pt = json_arr[0][0][-1]
        except:
            pt = None

        json_arr = json_arr[0][0][2]

        if pt.startswith("AssetsQuery"):
            return

        for partner_arr in json_arr:
            url = partner_arr[4]
            yield self.partner_asset_search_request_from_link(url)

        if pt is not None:
            yield self.partner_api_request_from_pt(pt)

    def parse_asset_search_html_page(self, response):
        js = response.xpath('//script[contains(text(), "INIT_data")]/text()').get()
        parsed = js2xml.parse(js)
        asset_links = parsed.xpath('//string[starts-with(text(), "/asset")]/text()')
        
        for al in asset_links:
            yield response.follow(al, callback=self.parse_asset_html_page)

        search_links = parsed.xpath('//string[starts-with(text(), "/search/asset")]/text()')
        
        for sl in search_links:
            yield response.follow(sl, callback=self.parse_asset_search_html_page)

        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))

        try:
            pt = parsed.xpath('//right/array/array/string[last()]/text()')[0]
        except:
            return

        if pt.startswith("AssetsQuery"):
            return

        params = {
            's': 24,
            'pt': pt,
            'hl': 'en',
            'rt': 'j'
        }
        
        if old_params.get('p') is not None:
            params['p'] = old_params['p']

        if old_params.get('em') is not None:
            params['em'] = old_params['em']

        url = 'https://artsandculture.google.com/api/assets/images?' + urlencode(params)
        yield scrapy.Request(url, callback=self.parse_asset_search_api_response)

    def parse_asset_search_api_response(self, response):
        json_str = response.text
        json_str = json_str[5:]

        json_arr = json.loads(json_str)
        
        json_str = response.text
        json_str = json_str[5:]

        json_arr = json.loads(json_str)
        
        try:
            pt = json_arr[0][0][-1]
        except:
            pt = None

        json_arr = json_arr[0][0][2]

        for asset_arr in json_arr:
            url = asset_arr[4]
            yield response.follow(url, callback=self.parse_asset_html_page)

        if pt.startswith("AssetsQuery"):
            return

        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))
        params = dict(old_params)
        params['pt'] = pt

        url = 'https://artsandculture.google.com/api/assets/images?' + urlencode(params)
        yield scrapy.Request(url, callback=self.parse_asset_search_api_response)

    def parse_asset_html_page(self, response):
        pass

