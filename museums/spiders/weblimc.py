import scrapy

import json
from urllib.parse import urlparse, parse_qsl, urlencode

from museums.items import ObjectItem

PER_PAGE = 100


class WeblimcSpider(scrapy.Spider):
    name = "weblimc"
    allowed_domains = ["www.salsah.org"]
    start_urls = ["https://www.salsah.org/api/selections/47/?lang=all"]

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0], callback=self.parse_selections_api_response
        )

    def parse_selections_api_response(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)

        for selection_dict in json_dict.get("selection", []):
            selection_id = selection_dict.get("id")

            params = {
                "searchtype": "extended",
                "filter_by_project": "LIMC",
                "show_nrows": str(PER_PAGE),
                "start_at": "0",
                "lang": "en",
                "filter_by_restype": "70",
                "property_id[]": "378",
                "compop[]": "EQ",
                "searchval[]": str(selection_id),
            }

            url = "https://www.salsah.org/api/search/?" + urlencode(params)
            yield scrapy.Request(url, callback=self.parse_search_api_response)

    def parse_search_api_response(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)

        for result in json_dict.get("subjects", []):
            obj_id = result.get("obj_id")
            obj_id = obj_id.split("_-_")[0]

            url = "https://www.salsah.org/api/graphdata/{}?full=1&lang=en".format(
                obj_id
            )
            yield scrapy.Request(url, callback=self.parse_graphdata_api_response)

        if len(json_dict.get("subjects", [])) < PER_PAGE:
            return

        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))

        params = dict(old_params)
        params["start_at"] = str(int(params["start_at"]) + PER_PAGE)

        next_page_url = "https://www.salsah.org/api/search/?" + urlencode(params)
        yield scrapy.Request(next_page_url, callback=self.parse_search_api_response)

    def extract_property_value(self, prop_dict, key):
        if prop_dict.get(key) is None:
            return None

        values = prop_dict.get(key).get("values")

        return "|".join(values)

    def parse_graphdata_api_response(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)

        item = ObjectItem()

        item["object_number"] = response.url.split("?")[0].split("/")[-1]

        for key, node_dict in (
            json_dict.get("graph", dict()).get("nodes", dict()).items()
        ):
            node_label = node_dict.get("resinfo", dict()).get("label")
            first_property = node_dict.get("resinfo", dict()).get("firstproperty")
            prop_dict = node_dict.get("properties")

            if node_label == "Museum":
                item["institution_name"] = self.extract_property_value(
                    prop_dict, "limc:name"
                )
                item["institution_city"] = self.extract_property_value(
                    prop_dict, "limc:city"
                )
                item["institution_country"] = self.extract_property_value(
                    prop_dict, "limc:country"
                )
            elif node_label == "Foto" and first_property == "1":
                item[
                    "image_url"
                ] = "https://www.salsah.org/core/sendlocdata.php?res={}&qtype=full&reduce=1".format(
                    key
                )
            elif node_label == "Szene":
                item["description"] = self.extract_property_value(
                    prop_dict, "limc:description"
                )
            elif node_label == "Monument":
                item["maker_full_name"] = self.extract_property_value(
                    prop_dict, "limc:artist"
                )
                item["category"] = self.extract_property_value(
                    prop_dict, "limc:category"
                )
                item["from_location"] = self.extract_property_value(
                    prop_dict, "limc:origin"
                )
                if item["from_location"] is None:
                    item["from_location"] = self.extract_property_value(
                        prop_dict, "limc:discovery"
                    )
                item["description"] = self.extract_property_value(
                    prop_dict, "limc:description"
                )
                item["technique"] = self.extract_property_value(
                    prop_dict, "limc:technique"
                )
                item["materials"] = self.extract_property_value(
                    prop_dict, "limc:material"
                )
                item["title"] = self.extract_property_value(prop_dict, "limc:scenename")
            elif node_label == "Datierung":
                item["date_description"] = self.extract_property_value(
                    prop_dict, "limc:period"
                )

        item["source_1"] = "https://weblimc.org/page/monument/" + item["object_number"]
        item["source_2"] = response.url

        yield item
