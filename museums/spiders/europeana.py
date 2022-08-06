import scrapy

import csv
import json
from urllib.parse import urlencode, urlparse, parse_qsl

from museums.items import ObjectItem


class EuropeanaSpider(scrapy.Spider):
    name = "europeana"
    allowed_domains = ["api.europeana.eu"]
    slugs = []

    def __init__(self):
        super().__init__()

        in_f = open("europeana_prep/filtered_orgs.csv", "r")
        csv_reader = csv.DictReader(in_f)

        for row in csv_reader:
            slug = row.get("slug")
            self.slugs.append(slug)

    def start_requests(self):
        for slug in self.slugs:
            inst_no = slug.split("-")[0]

            org_data_url = "http://data.europeana.eu/organization/" + inst_no

            params = {
                "wskey": "nLbaXYaiH",
                "cursor": "*",
                "qf": 'foaf_organization:"{}"'.format(org_data_url),
                "rows": "24",
                "query": 'foaf_organization:"{}"'.format(org_data_url),
                "profile": "minimal",
            }

            url = "https://api.europeana.eu/record/search.json?" + urlencode(params)
            yield scrapy.Request(url, callback=self.parse_search_api_response)

    def parse_search_api_response(self, response):
        json_dict = json.loads(response.text)

        for item_dict in json_dict.get("items", []):
            item = ObjectItem()

            item["object_number"] = item_dict.get("id")
            item["institution_name"] = item_dict.get("dataProvider")[0]

            if item_dict.get("edmPlaceLatitude") is not None and item_dict.get(
                "edmPlaceLongitude"
            ):
                lat1 = item_dict.get("edmPlaceLatitude")[0]
                lat1 = float(lat1)
                lat2 = item_dict.get("edmPlaceLatitude")[-1]
                lat2 = float(lat2)

                latitude = (lat1 + lat2) / 2.0

                lng1 = item_dict.get("edmPlaceLongitude")[0]
                lng1 = float(lng1)
                lng2 = item_dict.get("edmPlaceLongitude")[-1]
                lng2 = float(lng2)

                longitude = (lng1 + lng2) / 2.0

                item["institution_latitude"] = latitude
                item["institution_longitude"] = longitude

            # XXX: department, category
            item["title"] = item_dict.get("title")[0]
            item["description"] = " ".join(item_dict.get("dcDescription", []))
            # XXX: current_location, dimensions, inscription, provenance, materials,
            # technique, from_location, culture...

            if item_dict.get("edmIsShownBy") is not None:
                item["image_url"] = item_dict.get("edmIsShownBy")[0]

            link = item_dict.get("link")

            item["source_1"] = item_dict.get("guid")
            item["source_2"] = link

            yield scrapy.Request(
                link, callback=self.parse_record_api_response, meta={"item": item}
            )

        next_cursor = json_dict.get("nextCursor")
        if next_cursor is None:
            return

        o = urlparse(response.url)
        params = dict(parse_qsl(o.query))
        params["cursor"] = next_cursor

        url = "https://api.europeana.eu/record/search.json?" + urlencode(params)
        yield scrapy.Request(url, callback=self.parse_search_api_response)

    def parse_record_api_response(self, response):
        json_dict = json.loads(response.text)
        object_dict = json_dict.get("object", dict())

        item = response.meta.get("item")

        for proxy_dict in object_dict.get("proxies"):
            if proxy_dict.get("dcIdentifier") is not None:
                if type(proxy_dict.get("dcIdentifier")) == list:
                    item["object_number"] = proxy_dict.get("dcIdentifier")[-1]
                elif type(proxy_dict.get("dcIdentifier")) == dict:
                    item["object_number"] = proxy_dict.get("dcIdentifier").get("def")[0]

        yield item
