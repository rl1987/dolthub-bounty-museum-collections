import scrapy

import json
import logging

from scrapy.selector import Selector
from scrapy.http import FormRequest

from urllib.parse import urlencode, urlparse

class CentrepompidouSpider(scrapy.Spider):
    name = 'centrepompidou'
    allowed_domains = ['www.centrepompidou.fr']
    start_urls = ['http://www.centrepompidou.fr/']

    def start_requests(self):
        params = {
            'tx__[action]': 'ajaxSearch',
            'tx__[controller]': 'Recherche',
            'type': '7891012',
            'cHash': '00c2bdba7f2587e76c56cfc79343dc63',
        }

        data = {
            'resultsType': 'arts',
            'displayType': 'Grid',
            'terms': '',
            'page': '1',
            'sort': 'default',
        }

        logging.info(data)

        url = "https://www.centrepompidou.fr/en/recherche?" + urlencode(params)

        yield FormRequest(url, formdata=data, callback=self.parse_search_page, meta={'formdata': data})
    
    def parse_search_page(self, response):
        form_data = response.meta.get('formdata')
        form_data['page'] = str(int(form_data['page']) + 1)

        logging.info(form_data)

        json_str = response.text
        json_dict = json.loads(json_str)

        html_str = json_dict.get("resultsList")

        sel = Selector(text=html_str)

        for l in sel.xpath('//a/@href').getall():
            yield response.follow(l, callback=self.parse_object_page)

        yield FormRequest(response.url, formdata=form_data, callback=self.parse_search_page, meta={'formdata': form_data})

    def parse_object_page(self, response):
        pass

