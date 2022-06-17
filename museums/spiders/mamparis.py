import scrapy

from urllib.parse import urlparse, parse_qsl, urlencode
import json

class MamparisSpider(scrapy.Spider):
    name = 'mamparis'
    allowed_domains = ['mam.paris.fr', 'api.navigart.fr']
    start_urls = ['http://mam.paris.fr/']

    def start_requests(self):
        params = {
            'sort': 'by_author',
            'size': 60,
            'from': 0
        }

        url = 'https://api.navigart.fr/18/artworks?' + urlencode(params)

        yield scrapy.Request(url, callback=self.parse_search_results)
    
    def parse_search_results(self, response):
        json_dict = json.loads(response.text)

        results = json_dict.get("results")
        if results is None or len(results) == 0:
            return

        # TODO: parse data into items

        if len(results) < 60:
            return

        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))

        new_params = dict(old_params)

        new_params['from'] = int(new_params['from']) + 60

        url = 'https://api.navigart.fr/18/artworks?' + urlencode(new_params)

        yield scrapy.Request(url, callback=self.parse_search_results)

