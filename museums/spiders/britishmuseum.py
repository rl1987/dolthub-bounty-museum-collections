import scrapy

import json
from urllib.parse import urlparse, parse_qsl, urlencode

class BritishmuseumSpider(scrapy.Spider):
    name = 'britishmuseum'
    allowed_domains = ['britishmuseum.org']
    start_urls = ['https://www.britishmuseum.org/api/_search?&view=grid&sort=object_name__asc&page=0']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], method='POST', 
                callback=self.parse_search_api_response)

    def parse_search_api_response(self, response):
        json_dict = json.loads(response.text)
 
        hits = json_dict.get("hits", dict()).get("hits", [])

        for hit in hits:
            api_id = hit.get("_id")

            source_dict = hit.get("_source", dict())

            unique_object_id = None
            for id_dict in source_dict.get("identifier", []):
                if id_dict.get("type") == "unique object id":
                    unique_object_id = id_dict.get("unique_object_id")
                    break

            if unique_object_id is not None:
                url = "https://www.britishmuseum.org/api/_object?id=" + unique_object_id
                yield scrapy.Request(url, callback=self.parse_object_api_response)

        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))

        new_params = dict(old_params)
        new_params['page'] = int(new_params['page']) + 1

        next_page_url = 'https://www.britishmuseum.org/api/_search?&' + urlencode(new_params)

        yield scrapy.Request(next_page_url, method="POST", 
                callback=self.parse_search_api_response)

    def parse_object_api_response(self, response):
        pass


