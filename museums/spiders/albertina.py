import scrapy

from scrapy.http import JsonRequest
from scrapy.selector import Selector

import json
import logging

from museums.items import ObjectItem

PER_PAGE = 60


class AlbertinaSpider(scrapy.Spider):
    name = "albertina"
    allowed_domains = ["sammlungenonline.albertina.at"]
    start_urls = ["https://sammlungenonline.albertina.at/cc/ccConnector.asmx/search"]

    def start_requests(self):
        json_payload = {
            "authToken": "",
            "searchSpec": {
                "language": "gb",
                "fallbackLanguage": "de",
                "languageForEditor": "de",
                "ccSettingsName": "settings_gb",
                "numPerPage": PER_PAGE,
                "oldNumPerPage": PER_PAGE,
                "sortfields": {
                    "sortfield": [
                        {
                            "sortfield": "Dated",
                            "field": "/record/yearbegin_number",
                            "asc": True,
                        },
                        {
                            "sortfield": "Creator",
                            "field": "/record/creator/creatorsort",
                            "asc": True,
                        },
                        {
                            "sortfield": "Department",
                            "field": "/record/department/rank",
                            "asc": True,
                        },
                        {
                            "sortfield": "Inventory number",
                            "field": "/record/sortnumber",
                            "asc": True,
                        },
                    ],
                },
                "facetSort": {},
                "first": 1,
                "showtype": "icons",
                "oldShowtype": "icons",
                "searchscope": "All",
                "advancedSearchscope": "All",
                "customSearchscope": "All",
                "localbasket": [],
                "currentlyShowingAlbumId": "",
                "facetValues": {
                    "Datierung": {
                        "0": None,
                    },
                },
                "basketFilters": [],
                "queryFilters": [],
                "filters": [],
                "searchValuesAdvanced": [],
                "searchValuesCustom": [],
                "searchValuesProfessional": [],
                "searchValuesAdvanced2": {
                    "id": "6abf5f58-1071-43e6-b31e-eb746f68d5a4",
                    "subqueries": [
                        {
                            "id": "4a86b550-c1f6-4031-8101-32e7ba27874c",
                            "searchscope": "",
                            "field": "KÜNSTLER_IN",
                            "value": "",
                            "queryoperator": "and",
                            "rangeField": {
                                "low": None,
                                "high": None,
                            },
                            "minValue": None,
                            "maxValue": None,
                        },
                    ],
                    "searchscope": "All",
                    "queryoperator": "and",
                },
                "searchValues": [
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 0,
                        "tag": "KÜNSTLER_IN",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 1,
                        "tag": "All search fields",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 2,
                        "tag": "Title or name",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 3,
                        "tag": "Object number",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 4,
                        "tag": "Geografischer Bezug",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 5,
                        "tag": "Date/Year",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 6,
                        "tag": "Gattung",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 7,
                        "tag": "Technik",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 8,
                        "tag": "Provenienz",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 9,
                        "tag": "Serie / Zyklus",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 10,
                        "tag": "Stifter / Leihgeber",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 11,
                        "tag": "Stempel / stamps",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 12,
                        "tag": "Wasserzeichen",
                        "value": "",
                        "searchOperator": "and",
                    },
                    {
                        "searchscope": {
                            "scopeName": "All",
                            "scopeTag": "",
                        },
                        "id": 13,
                        "tag": "COLLECTION",
                        "value": "",
                        "searchOperator": "and",
                    },
                ],
                "showingRecordViewTab": "",
                "orderFormType": "less1200",
                "filename": "",
                "articlename": "",
            },
        }

        logging.debug(json_payload)

        yield JsonRequest(
            self.start_urls[0],
            data=json_payload,
            callback=self.parse_search_page,
            meta={"json_payload": json_payload},
        )

    def get_selector(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)

        html_str = json_dict.get("d", dict()).get("result")
        if html_str is None:
            return

        sel = Selector(text=html_str)

        return sel

    def parse_search_page(self, response):
        sel = self.get_selector(response)
        ng_clicks = sel.xpath(
            '//*[starts-with(@ng-click, "jumpToRecord")]/@ng-click'
        ).getall()
        for ng_click in ng_clicks:
            item_no = ng_click.replace("jumpToRecord('", "").replace("')", "")

            json_payload = {
                "authToken": "",
                "searchSpec": {
                    "language": "gb",
                    "fallbackLanguage": "de",
                    "languageForEditor": "de",
                    "ccSettingsName": "settings_gb",
                    "numPerPage": 1,
                    "oldNumPerPage": 12,
                    "sortfields": {
                        "sortfield": [
                            {
                                "sortfield": "Dated",
                                "field": "/record/yearbegin_number",
                                "asc": True,
                            },
                            {
                                "sortfield": "Creator",
                                "field": "/record/creator/creatorsort",
                                "asc": True,
                            },
                            {
                                "sortfield": "Department",
                                "field": "/record/department/rank",
                                "asc": True,
                            },
                            {
                                "sortfield": "Inventory number",
                                "field": "/record/sortnumber",
                                "asc": True,
                            },
                        ],
                    },
                    "facetSort": {},
                    "first": item_no,
                    "showtype": "record",
                    "oldShowtype": "icons",
                    "searchscope": "All",
                    "advancedSearchscope": "All",
                    "customSearchscope": "All",
                    "localbasket": [],
                    "currentlyShowingAlbumId": "",
                    "facetValues": {
                        "Datierung": {
                            "0": None,
                        },
                    },
                    "basketFilters": [],
                    "queryFilters": [],
                    "filters": [],
                    "searchValuesAdvanced": [],
                    "searchValuesCustom": [],
                    "searchValuesProfessional": [],
                    "searchValuesAdvanced2": {
                        "id": "6abf5f58-1071-43e6-b31e-eb746f68d5a4",
                        "subqueries": [
                            {
                                "id": "4a86b550-c1f6-4031-8101-32e7ba27874c",
                                "searchscope": "",
                                "field": "KÜNSTLER_IN",
                                "value": "",
                                "queryoperator": "and",
                                "rangeField": {
                                    "low": None,
                                    "high": None,
                                },
                                "minValue": None,
                                "maxValue": None,
                            },
                        ],
                        "searchscope": "All",
                        "queryoperator": "and",
                    },
                    "searchValues": [
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 0,
                            "tag": "KÜNSTLER_IN",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 1,
                            "tag": "All search fields",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 2,
                            "tag": "Title or name",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 3,
                            "tag": "Object number",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 4,
                            "tag": "Geografischer Bezug",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 5,
                            "tag": "Date/Year",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 6,
                            "tag": "Gattung",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 7,
                            "tag": "Technik",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 8,
                            "tag": "Provenienz",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 9,
                            "tag": "Serie / Zyklus",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 10,
                            "tag": "Stifter / Leihgeber",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 11,
                            "tag": "Stempel / stamps",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 12,
                            "tag": "Wasserzeichen",
                            "value": "",
                            "searchOperator": "and",
                        },
                        {
                            "searchscope": {
                                "scopeName": "All",
                                "scopeTag": "",
                            },
                            "id": 13,
                            "tag": "COLLECTION",
                            "value": "",
                            "searchOperator": "and",
                        },
                    ],
                    "showingRecordViewTab": "",
                    "orderFormType": "less1200",
                    "filename": "",
                    "articlename": "",
                },
            }

            logging.debug(json_payload)

            yield JsonRequest(
                self.start_urls[0], data=json_payload, callback=self.parse_artwork_page
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
            meta={"json_payload": json_payload},
        )

    def parse_artwork_page(self, response):
        sel = self.get_selector(response)

        item = ObjectItem()

        item["object_number"] = sel.xpath(
            '//div[text()="Inventory number"]/following-sibling::div/text()'
        ).get()
        item["institution_name"] = "Albertina"
        item["institution_city"] = "Vienna"
        item["institution_state"] = "Vienna"
        item["institution_country"] = "Austria"
        item["institution_latitude"] = 48.2046992
        item["institution_longitude"] = 16.3659937
        # XXX: department
        item["category"] = sel.xpath(
            '//div[text()="Object category"]/following-sibling::div/text()'
        ).get()
        item["title"] = sel.xpath('//div[@class="recordViewRecordTitle"]/text()').get()
        # XXX: current_location, dimensions, inscription
        item["description"] = " ".join(
            sel.xpath('//div[@class="recordViewRecordfieldValueSmall"]/text()').getall()
        )
        item["provenance"] = sel.xpath(
            '//div[text()="Provenance"]/following-sibling::div/text()'
        ).get()
        # XXX: materials
        item["technique"] = sel.xpath(
            '//div[text()="Technique"]/following-sibling::div/text()'
        ).get()
        # XXX: from_location, culture, date...
        item["maker_full_name"] = "|".join(
            sel.xpath(
                '//div[contains(@class, "recordViewTabInner")]//span[@class="recordViewRecordfieldValueHyperlinked"]/text()'
            ).getall()
        )
        item["credit_line"] = sel.xpath(
            '//span[text()="Bibliography"]/following-sibling::div/text()'
        ).get()
        item["image_url"] = sel.xpath('//img[@class="img-responsive"]/@src').get()
        item["source_1"] = sel.xpath(
            '//div[text()="Permalink"]/following-sibling::div/text()'
        ).get()

        yield item
