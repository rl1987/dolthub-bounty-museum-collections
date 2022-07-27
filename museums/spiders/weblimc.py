import scrapy

import json
from urllib.parse import urlparse, parse_qsl, urlencode

PER_PAGE = 100

class WeblimcSpider(scrapy.Spider):
    name = 'weblimc'
    allowed_domains = ['www.salsah.org']
    start_urls = ['https://www.salsah.org/api/selections/47/?lang=all']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_selections_api_response)
    
    def parse_selections_api_response(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)
        
        for selection_dict in json_dict.get("selection", []):
            selection_id = selection_dict.get("id")

            params = {
                'searchtype': 'extended',
                'filter_by_project': 'LIMC',
                'show_nrows': str(PER_PAGE),
                'start_at': '0',
                'lang': 'en',
                'filter_by_restype': '70',
                'property_id[]': '378',
                'compop[]': 'EQ',
                'searchval[]': str(selection_id)
            }

            url = 'https://www.salsah.org/api/search/?' + urlencode(params)
            yield scrapy.Request(url, callback=self.parse_search_api_response)

    def parse_search_api_response(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)

        for result in json_dict.get("subjects", []):
            obj_id = result.get("obj_id")
            obj_id = obj_id.split("_-_")[0]

            url = "https://www.salsah.org/api/graphdata/{}?full=1&lang=en".format(obj_id)
            yield scrapy.Request(url, callback=self.parse_graphdata_api_response)

        if len(json_dict.get("subjects", [])) < PER_PAGE:
            return

        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))

        params = dict(params)
        params['start_at'] = str(int(params['start_at'] + PER_PAGE))

        next_page_url = 'https://www.salsah.org/api/search/?' + urlencode(params)
        yield scrapy.Request(next_page_url, callback=self.parse_search_api_response)

    def parse_graphdata_api_response(self, response):
        pass

