import scrapy
from scrapy.http import JsonRequest

from urllib.parse import urlencode, urlparse, parse_qsl
import json

from museums.items import ObjectItem

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

        if len(json_dict.get("results", [])) < 10:
            return

        next_page_url = json_dict.get("next")
        if next_page_url is not None:
            yield scrapy.Request(next_page_url, callback=self.parse_search_page, headers={'Accept': 'application/json'})

    def parse_object_page(self, response):
        json_dict = json.loads(response.text)
        payload = json_dict.get("payload", dict())

        item = ObjectItem()

        item['object_number'] = payload.get("main_ref_no", dict()).get("number")
        if item['object_number'] is None:
            item['object_number'] = payload.get("idno")
        item['institution_name'] = 'Museum of Archaelogy and Anthropology'
        item['institution_city'] = 'Cambridge'
        item['institution_state'] = ''
        item['institution_country'] = 'United Kingdom'
        item['institution_latitude'] = 52.2028961
        item['institution_longitude'] = 0.1208059
        item['department'] = payload.get("department", dict()).get("name")
        item['title'] = payload.get("description")
        if item['title'] is not None:
            item['title'] = item['title'].replace("<br />", " ")
        item['description'] = payload.get("de_norm_event_description")
        if item['description'] is not None:
            item['description'] = item['description'].replace("<br />", " ")
        item['dimensions'] = payload.get("dimensions")
        item['materials'] = "|".join(list(map(lambda m: m.get("name"), payload.get("material", []))))
        item['technique'] = payload.get("format", dict()).get("name")
        item['from_location'] = payload.get("de_norm_place")
        item['culture'] = "|".join(list(map(lambda c: c.get("name"), payload.get("culture_group", []))))
        if payload.get("date") is not None:
            item['date_description'] = payload.get('date')
        else:
            item['date_description'] = "; ".join(list(map(lambda p: p.get("name"), payload.get("period"))))
        if payload.get("photographer") is not None:
            item['maker_full_name'] = payload.get("photographer", dict()).get("name")

        if type(payload.get("source")) == str:
            item['acquired_from'] = payload.get("source")
        elif type(payload.get("source")) == dict:
            item['acquired_from'] = payload.get('source').get('name')
        item['accession_number'] = payload.get("main_ref_no", dict()).get("number")
        if item['accession_number'] is None and payload.get("collections_accession") is not None:
            item['accession_number'] = payload.get("collections_accession", dict()).get("number")
        if payload.get("main_image") is not None:
            item['image_url'] = payload.get("main_image", dict()).get("image")
        item['source_1'] = 'https://collections.maa.cam.ac.uk/objects/' + str(payload.get('id'))

        yield item

