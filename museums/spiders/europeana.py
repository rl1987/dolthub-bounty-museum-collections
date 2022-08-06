import scrapy

import json
from urllib.parse import urlencode, urlparse, parse_qsl

class EuropeanaSpider(scrapy.Spider):
    name = 'europeana'
    allowed_domains = ['api.europeana.eu']
    slugs = []

    def __init__(self):
        super().__init__()

        self.slugs = [ '1482250000004516027-tartu-art-museum' ]

    def start_requests(self):
        for slug in self.slugs:
            inst_no = slug.split("-")[0]

            org_data_url = "http://data.europeana.eu/organization/" + inst_no
            
            params = {
                'wskey': "nLbaXYaiH",
                "cursor": "*",
                "qf": 'foaf_organization:"{}"'.format(org_data_url),
                "rows": "24",
                "query": 'foaf_organization:"{}"'.format(org_data_url),
                "profile": "minimal"
            }

            url = "https://api.europeana.eu/record/search.json?" + urlencode(params)
            yield scrapy.Request(url, callback=self.parse_search_api_response)

    def parse_search_api_response(self, response):
        json_dict = json.loads(response.text)
    
        for item_dict in json_dict.get("items", []):
            link = item_dict.get("link")
            yield scrapy.Request(link, callback=self.parse_record_api_response)

        next_cursor = json_dict.get("nextCursor")
        if next_cursor is None:
            return

        o = urlparse(response.url)
        params = dict(parse_qsl(o.query))
        params['cursor'] = next_cursor

        url = "https://api.europeana.eu/record/search.json?" + urlencode(params)
        yield scrapy.Request(url, callback=self.parse_search_api_response)

    def parse_record_api_response(self, response):
        pass

