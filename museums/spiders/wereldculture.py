import scrapy
from scrapy.http import JsonRequest
from scrapy.selector import Selector

import logging
import json
from urllib.parse import urljoin

from museums.items import ObjectItem

PER_PAGE = 12


class WereldcultureSpider(scrapy.Spider):
    name = "wereldculture"
    allowed_domains = ["collectie.wereldculturen.nl"]
    start_urls = ["https://collectie.wereldculturen.nl/cc/ccConnector.asmx/search"]
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://collectie.wereldculturen.nl",
        "Pragma": "no-cache",
        "Referer": "https://collectie.wereldculturen.nl/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    def start_requests(self):
        json_payload = {
            "authToken": "",
            "searchSpec": {
                "language": "nl",
                "fallbackLanguage": "en",
                "languageForEditor": "en",
                "ccSettingsName": "Alternative",
                "numPerPage": PER_PAGE,
                "oldNumPerPage": PER_PAGE,
                "sortfields": {
                    "sortfield": [
                        {
                            "sortfield": "Now on display",
                            "field": "/record/ondisplayfacet",
                            "asc": True,
                        },
                        {"sortfield": "Relevance", "field": "ccRelevance", "asc": True},
                        {"sortfield": "Title", "field": "", "asc": True},
                        {
                            "sortfield": "Object number",
                            "field": "/record/sortnumber",
                            "asc": True,
                        },
                        {
                            "sortfield": "Dated",
                            "field": "/record/datebegin",
                            "asc": True,
                        },
                        {
                            "sortfield": "Name",
                            "field": "/record/creator/alphasort",
                            "asc": True,
                        },
                    ]
                },
                "facetSort": {},
                "first": 1,
                "showtype": "icons",
                "oldShowtype": "icons",
                "searchscope": "Search the whole record",
                "advancedSearchscope": "Search the whole record",
                "customSearchscope": "Search the whole record",
                "currentlyShowingAlbumId": "",
                "facetValues": {},
                "basketFilters": [],
                "queryFilters": [],
                "filters": [],
                "searchValuesAdvanced": [],
                "searchValuesCustom": [],
                "searchValuesProfessional": [],
                "searchValuesAdvanced2": {
                    "id": "50ce2f2b-eec5-4748-8d75-094b7ab25364",
                    "subqueries": [
                        {
                            "id": "95847310-3a6f-4748-8005-6edd2e01a9bc",
                            "searchscope": "",
                            "field": "All fields",
                            "value": "",
                            "queryoperator": "and",
                        }
                    ],
                    "searchscope": "Search the whole record",
                    "queryoperator": "and",
                },
                "searchValues": [
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 0,
                        "tag": "All fields",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 1,
                        "tag": "Object number",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 2,
                        "tag": "Title(s)",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 3,
                        "tag": "Objectname",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 4,
                        "tag": "Description",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 5,
                        "tag": "Constituents",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 6,
                        "tag": "Medium",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 7,
                        "tag": "Dimensions",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 8,
                        "tag": "Dated",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 9,
                        "tag": "Signed",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 10,
                        "tag": "Inscribed",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 11,
                        "tag": "Markings",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 12,
                        "tag": "Functional category",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 13,
                        "tag": "Geographical origin",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 14,
                        "tag": "Cultural origin",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 15,
                        "tag": "Religion",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 16,
                        "tag": "Styles and periods",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 17,
                        "tag": "Materials and technic",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 18,
                        "tag": "Object keyword",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 19,
                        "tag": "Presentation keyword",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 20,
                        "tag": "Bibliography",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 21,
                        "tag": "Literature",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 22,
                        "tag": "Related objects",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 23,
                        "tag": "Classification",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 24,
                        "tag": "Now on display",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 25,
                        "tag": "Creditline",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 26,
                        "tag": "Names",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 27,
                        "tag": "Nationality",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 28,
                        "tag": "Position",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 29,
                        "tag": "Begin date",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 30,
                        "tag": "End date",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 31,
                        "tag": "Curatorial notes",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 32,
                        "tag": "Deeplink identifier",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 33,
                        "tag": "Theme Mentawai",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "Search the whole record",
                            "scopeTag": "",
                        },
                        "id": 34,
                        "tag": "Thesaurus",
                        "value": "",
                        "searchOperator": "and",
                    },
                ],
                "filename": "",
                "articlename": "",
            },
        }

        logging.debug(json_payload)

        yield JsonRequest(
            self.start_urls[0],
            data=json_payload,
            callback=self.parse_search_page,
            headers=self.headers,
            meta={"json_payload": json_payload},
        )

    def get_selector_from_response(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)
        html_str = json_dict.get("d", dict()).get("result")
        if html_str is None:
            return

        sel = Selector(text=html_str)
        return sel

    def parse_search_page(self, response):
        sel = self.get_selector_from_response(response)
        if sel is None:
            return

        ng_clicks = sel.xpath(
            '//*[starts-with(@ng-click, "jumpToRecord")]/@ng-click'
        ).getall()
        for ng_click in ng_clicks:
            item_no = ng_click.replace("jumpToRecord('", "").replace("');", "")

            json_payload = {
                "authToken": "",
                "searchSpec": {
                    "language": "nl",
                    "fallbackLanguage": "en",
                    "languageForEditor": "en",
                    "ccSettingsName": "Alternative",
                    "numPerPage": 1,
                    "oldNumPerPage": 12,
                    "sortfields": {
                        "sortfield": [
                            {
                                "sortfield": "Now on display",
                                "field": "/record/ondisplayfacet",
                                "asc": True,
                            },
                            {
                                "sortfield": "Relevance",
                                "field": "ccRelevance",
                                "asc": True,
                            },
                            {
                                "sortfield": "Title",
                                "field": "",
                                "asc": True,
                            },
                            {
                                "sortfield": "Object number",
                                "field": "/record/sortnumber",
                                "asc": True,
                            },
                            {
                                "sortfield": "Dated",
                                "field": "/record/datebegin",
                                "asc": True,
                            },
                            {
                                "sortfield": "Name",
                                "field": "/record/creator/alphasort",
                                "asc": True,
                            },
                        ],
                    },
                    "facetSort": {},
                    "first": str(item_no),
                    "showtype": "record",
                    "oldShowtype": "icons",
                    "searchscope": "Search the whole record",
                    "advancedSearchscope": "Search the whole record",
                    "customSearchscope": "Search the whole record",
                    "currentlyShowingAlbumId": "",
                    "facetValues": {},
                    "basketFilters": [],
                    "queryFilters": [],
                    "filters": [],
                    "searchValuesAdvanced": [],
                    "searchValuesCustom": [],
                    "searchValuesProfessional": [],
                    "searchValuesAdvanced2": {
                        "id": "50ce2f2b-eec5-4748-8d75-094b7ab25364",
                        "subqueries": [
                            {
                                "id": "95847310-3a6f-4748-8005-6edd2e01a9bc",
                                "searchscope": "",
                                "field": "All fields",
                                "value": "",
                                "queryoperator": "and",
                            },
                        ],
                        "searchscope": "Search the whole record",
                        "queryoperator": "and",
                    },
                    "searchValues": [
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 0,
                            "tag": "All fields",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 1,
                            "tag": "Object number",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 2,
                            "tag": "Title(s)",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 3,
                            "tag": "Objectname",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 4,
                            "tag": "Description",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 5,
                            "tag": "Constituents",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 6,
                            "tag": "Medium",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 7,
                            "tag": "Dimensions",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 8,
                            "tag": "Dated",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 9,
                            "tag": "Signed",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 10,
                            "tag": "Inscribed",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 11,
                            "tag": "Markings",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 12,
                            "tag": "Functional category",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 13,
                            "tag": "Geographical origin",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 14,
                            "tag": "Cultural origin",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 15,
                            "tag": "Religion",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 16,
                            "tag": "Styles and periods",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 17,
                            "tag": "Materials and technic",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 18,
                            "tag": "Object keyword",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 19,
                            "tag": "Presentation keyword",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 20,
                            "tag": "Bibliography",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 21,
                            "tag": "Literature",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 22,
                            "tag": "Related objects",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 23,
                            "tag": "Classification",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 24,
                            "tag": "Now on display",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 25,
                            "tag": "Creditline",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 26,
                            "tag": "Names",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 27,
                            "tag": "Nationality",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 28,
                            "tag": "Position",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 29,
                            "tag": "Begin date",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 30,
                            "tag": "End date",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 31,
                            "tag": "Curatorial notes",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 32,
                            "tag": "Deeplink identifier",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 33,
                            "tag": "Theme Mentawai",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "Search the whole record",
                                "scopeTag": "",
                            },
                            "id": 34,
                            "tag": "Thesaurus",
                            "value": "",
                            "searchOperator": "and",
                        },
                    ],
                    "filename": "",
                    "articlename": "",
                },
            }

            logging.debug(json_payload)

            yield JsonRequest(
                self.start_urls[0],
                data=json_payload,
                headers=self.headers,
                callback=self.parse_object_page,
            )

        if len(ng_clicks) < PER_PAGE:
            return

        json_payload = response.meta.get("json_payload")
        json_payload["searchSpec"]["first"] += PER_PAGE

        logging.debug(json_payload)

        yield JsonRequest(
            self.start_urls[0],
            data=json_payload,
            callback=self.parse_search_page,
            headers=self.headers,
            meta={"json_payload": json_payload},
        )

    def parse_object_page(self, response):
        sel = self.get_selector_from_response(response)
        if sel is None:
            return

        item = ObjectItem()

        item["object_number"] = sel.xpath(
            '//strong[text()="Object number : " or text()="Inventarisnummer : "]/following-sibling::text()'
        ).get()
        item["institution_name"] = "The National Museum of World Cultures"
        item["institution_city"] = "Amsterdam"
        item["institution_state"] = ""
        item["institution_country"] = "Netherlands"
        item["institution_latitude"] = 52.3626561
        item["institution_longitude"] = 4.9211787
        item["title"] = "".join(sel.xpath('//div[@ng-if="cc.language==\'en\'"]/h3[@data-drag="true"]//text()').getall()).strip()
        
        lines = sel.xpath('//div[@class="panel-body"]/div[@ng-if="cc.language==\'en\'"]//text()').getall()

        item["description"] = " ".join(lines).strip().split("{{userdata.baskets[$basketIndex].description}}")[0]

        for i in range(0, len(lines)-1):
            l = lines[i]
            if l == "Origin : " or l == "Herkomst : ":
                item['provenance'] = lines[i+1]
            elif l == "Medium : " or l == "Materiaal : ":
                item['materials'] = lines[i+1]
            elif l == "Culture : " or l == "Cultuur : ":
                item['culture'] = lines[i+1]
            elif l == "Creditline : ":
                item['credit_line'] = lines[i+1]

        item["source_1"] = sel.xpath(
            '//div[./b[text()="Permanent link to this object : "]]/text()'
        ).get()

        item["image_url"] = sel.xpath(
            '//*[@data-drag="true"]/@data-draggingimage'
        ).get()
        if item["image_url"] is not None:
            item["image_url"] = urljoin(
                response.url, "/" + item["image_url"].split("&width")[0]
            )

        yield item
