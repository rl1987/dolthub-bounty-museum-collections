import scrapy
from scrapy.selector import Selector

import json
from urllib.parse import urlparse, parse_qsl, urlencode

from museums.items import ObjectItem

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
        json_dict = json.loads(response.text)
        source_dict = json_dict.get("hits", dict()).get("hits")[0].get("_source")

        o = urlparse(response.url)

        params = dict(parse_qsl(o.query))

        item = ObjectItem()

        item['object_number'] = params.get("id")
        
        item['institution_name'] = 'British Museum'
        item['institution_city'] = 'London'
        item['institution_country'] = 'United Kingdom'
        item['institution_latitude'] = 51.518757
        item['institution_longitude'] = -0.126168
        
        # XXX: category

        xtemplate_full_json_str = source_dict.get("xtemplate", dict()).get("full")
        xtemplate_full_json_dict = json.loads(xtemplate_full_json_str)

        if type(xtemplate_full_json_dict.get("Title")) == list:
            title_parts = []

            for title_html in xtemplate_full_json_dict.get("Title", []):
                sel = Selector(text=title_html)
                title_part = " ".join(sel.xpath("//text()").getall())
                title_parts.append(title_part)

            item['title'] = " ".join(title_parts)
        elif type(xtemplate_full_json_dict.get("Title")) == str:
            title_html = xtemplate_full_json_dict.get("Title")
            sel = Selector(text=title_html)
            item['title'] = " ".join(sel.xpath("//text()").getall())

        item['department'] = xtemplate_full_json_dict.get("Department")
        item['description'] = " ".join(xtemplate_full_json_dict.get("Description", []))
        item['current_location'] = xtemplate_full_json_dict.get("Location")
        
        dimensions = []

        for dimension_html in xtemplate_full_json_dict.get("Dimensions", []):
            sel = Selector(text=dimension_html)
            dimension = " ".join(sel.xpath("//text()").getall())
            dimensions.append(dimension)

        item['dimensions'] = "|".join(dimensions)

        item['source_1'] = 'https://www.britishmuseum.org/collection/object/' + params.get("id")
        item['source_2'] = response.url

        yield item
