import scrapy

import json
from urllib.parse import urlparse, urlencode, parse_qsl

# https://collections.vam.ac.uk/search/?page=1&page_size=15

class VictoriaNAlbertSpider(scrapy.Spider):
    name = 'victorianalbert'
    allowed_domains = ['api.vam.ac.uk', 'collections.vam.ac.uk']

    def start_requests(self):
        params = {
            "page": 1,
            "page_size": 50
        }

        url = "https://api.vam.ac.uk/v2/objects/search?" + urlencode(params)

        yield scrapy.Request(url, callback=self.parse_clusters)

    def recursively_generate_requests(self, clusters, params):
        n_cluster_keys = len(clusters)

        key = list(clusters.keys())[0]
        
        if n_cluster_keys == 1:
            for value in clusters.get(key):
                new_params = dict(params)
                new_params[key] = value

                url = "https://api.vam.ac.uk/v2/objects/search?" + urlencode(new_params)
                yield scrapy.Request(url, callback=self.parse_search_page)
        else:
            new_clusters = dict(clusters)
            del new_clusters[key]

            for value in clusters.get(key):
                new_params = dict(params)
                new_params[key] = value

                for request in self.recursively_generate_requests(new_clusters, new_params):
                    yield request

    def parse_clusters(self, response):
        json_dict = json.loads(response.text)

        clusters = dict()

        for cname, cdict in json_dict.get("clusters").items():
            clusters["id_" + cname] = list(map(lambda term: term.get("id"), cdict.get("terms")))

        self.logger.debug(clusters)
 
        params = {
            "page": 1,
            "page_size": 50
        }

        for request in self.recursively_generate_requests(clusters, params):
            self.logger.info(request)

    def parse_search_page(self, response):
        pass

    def parse_object_page(self, response):
        pass

