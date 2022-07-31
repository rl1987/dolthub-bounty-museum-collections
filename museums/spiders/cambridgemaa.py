import scrapy
from scrapy.http import JsonRequest

from urllib.parse import urlencode, urlparse, parse_qsl
import json

class CambridgemaaSpider(scrapy.Spider):
    name = 'cambridgemaa'
    allowed_domains = ['collections.maa.cam.ac.uk']

    def start_requests(self):
        query_dict = {
            "string": "",
            "options": [],
            "currentPage": 1,
            "filters": []
        }

        params = {
            'query': json.dumps(query_dict)
        }

        url1 = 'https://collections.maa.cam.ac.uk/objects-api/objects/?' + urlencode(params)
        yield scrapy.Request(url1, callback=self.parse_search_page, headers={'Accept': 'application/json'})

        url2 = 'https://collections.maa.cam.ac.uk/photographs-api/photographs/?' + urlencode(params)
        yield scrapy.Request(url2, callback=self.parse_search_page, headers={'Accept': 'application/json'})

    def parse_search_page(self, response):
        json_dict = json.loads(response.text)
        
        for result_dict in json_dict.get("results", []):
            result_id = result_dict.get("id")
            json_payload = { "id": str(result_id) }
            if "photographs-api" in response.url:
                url = "https://collections.maa.cam.ac.uk/photographs-api/get-item/"
            else:
                url = "https://collections.maa.cam.ac.uk/objects-api/get-item/"

            yield JsonRequest(url, data=json_payload, callback=self.parse_object_page, dont_filter=True)

        o = urlparse(response.url)
        params = dict(parse_qsl(o.query))
        query_dict = json.loads(params['query'])
        query_dict['currentPage'] += 1
        params['query'] = json.dumps(query_dict)
        next_page_url = o.scheme + '://' + o.netloc + o.path + '?' + urlencode(params)
        yield scrapy.Request(next_page_url, callback=self.parse_search_page, headers={'Accept': 'application/json'})

    def parse_object_page(self, response):
        pass

