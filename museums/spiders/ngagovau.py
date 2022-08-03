import scrapy

import json
from urllib.parse import urljoin

from scrapy.http import JsonRequest
from scrapy.selector import Selector

from museums.items import ObjectItem


class NgagovauSpider(scrapy.Spider):
    name = "ngagovau"
    allowed_domains = ["searchthecollection.nga.gov.au"]
    start_urls = ["https://searchthecollection.nga.gov.au/stcapi/service/stc/search"]

    def start_requests(self):
        json_data = {
            "includeParts": None,
            "searchIn": [],
            "selectedFilters": [],
            "pageSize": 50,
            "retainSearch": True,
            "keyword": "*",
            "startIndex": 0,
            "facetedSearch": {
                "objectType": {
                    "terms": {
                        "field": "objectTypeFacet",
                        "limit": 3,
                    },
                },
                "location": {
                    "terms": {
                        "field": "locationFacet",
                        "limit": 3,
                    },
                },
                "place": {
                    "terms": {
                        "field": "placeOfCreationFacet",
                        "limit": 3,
                    },
                },
                "creators": {
                    "terms": {
                        "field": "creatorsFacet",
                        "limit": 5,
                    },
                },
                "woaWithImage": {
                    "query": "defaultThumbnail:*",
                },
            },
        }

        yield JsonRequest(
            self.start_urls[0],
            data=json_data,
            callback=self.parse_search_api_response,
            meta={"json_data": json_data},
        )

    def parse_search_api_response(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)

        items = json_dict.get("payLoad", dict()).get("items", [])

        for item_dict in items:
            item = ObjectItem()

            item["object_number"] = str(item_dict.get("irn"))
            item["institution_name"] = "National Gallery Australia"
            item["institution_city"] = "Parkes"
            item["institution_state"] = "ACT"
            item["institution_country"] = "Australia"
            item["institution_latitude"] = -35.287122
            item["institution_longitude"] = 149.1050016
            item["department"] = item_dict.get("deparment")
            item["inscription"] = item_dict.get("vraInscriptionDisplayText")
            item["category"] = "|".join(item_dict.get("objectType", []))
            item["title"] = item_dict.get("woaCmTitle")
            item["dimensions"] = item_dict.get("measurementDetailsJson")
            item["provenance"] = item_dict.get("provenance")
            item["materials"] = "|".join(item_dict.get("materials", []))
            item["technique"] = "|".join(item_dict.get("techniques", []))
            item["from_location"] = "|".join(item_dict.get("placeOfCreation", []))
            item["date_description"] = item_dict.get("vraDateDisplayText")

            try:
                item["year_start"] = int(
                    item_dict.get("creEarliestDate", "").split("-")[0]
                )
                item["year_end"] = int(item_dict.get("creLatestDate", "").split("-")[0])
            except:
                pass

            creators_json_str = item_dict.get("creatorsJson")
            if creators_json_str is not None:
                creators_json_arr = json.loads(creators_json_str)

                maker_birth_years = []
                maker_death_years = []
                maker_names = []
                maker_roles = []

                for creator_dict in creators_json_arr:
                    birth_year = creator_dict.get("BioBirthEarliestDate", "")
                    maker_birth_years.append(birth_year)
                    death_year = creator_dict.get("BioDeathEarliestDate", "")
                    maker_death_years.append(death_year)
                    name = creator_dict.get("NamFullName", "")
                    maker_names.append(name)
                    role = creator_dict.get("CreRole_tab", "")
                    maker_roles.append(role)

                item["maker_birth_year"] = "|".join(maker_birth_years)
                item["maker_death_year"] = "|".join(maker_death_years)
                item["maker_full_name"] = "|".join(maker_names)
                item["maker_role"] = "|".join(maker_roles)
            else:
                item["maker_full_name"] = "|".join(item_dict.get("creators", []))
                item["maker_role"] = "|".join(item_dict.get("roles", []))

            try:
                item["accession_year"] = int(
                    item_dict.get("accessionMeetingDate", "").split("-")[0]
                )
            except:
                pass
            item["accession_number"] = item_dict.get("vraIdentifier")
            item["credit_line"] = item_dict.get("accessionCreditLine")
            item[
                "source_1"
            ] = "https://searchthecollection.nga.gov.au/object?uniqueId=" + str(
                item["object_number"]
            )
            item["source_2"] = (
                "https://searchthecollection.nga.gov.au/stcapi/service/stc/node?uniqueId="
                + str(item["object_number"])
            )

            thumbnail_json_str = item_dict.get("defaultThumbnail", "{}")
            thumbnail_json_dict = json.loads(thumbnail_json_str)
            preview_url = thumbnail_json_dict.get("imgpreview")
            if preview_url is not None:
                item["image_url"] = (
                    "https://searchthecollection.nga.gov.au/stcapi/service/ngacd/asset/preview?contentInfo="
                    + preview_url
                )

            url = (
                "https://searchthecollection.nga.gov.au/stcapi/service/ngacd/narratives?uniqueId="
                + item["object_number"]
            )
            yield scrapy.Request(
                url, meta={"item": item}, callback=self.parse_narrative_api_response
            )

        n_total = json_dict.get("payLoad", dict()).get("totalRecordsUpper")

        json_data = response.meta.get("json_data")
        per_page = json_data.get("pageSize")
        start_idx = json_data.get("startIndex")

        if start_idx + per_page < n_total:
            start_idx += per_page
            json_data["startIndex"] = start_idx
            yield JsonRequest(
                self.start_urls[0],
                data=json_data,
                callback=self.parse_search_api_response,
                meta={"json_data": json_data},
            )

    def parse_narrative_api_response(self, response):
        item = response.meta.get("item")

        json_str = response.text
        json_dict = json.loads(json_str)
        payload = json_dict.get("payLoad", [])
        if len(payload) > 0:
            html_str = payload[0].get("narNarrative", "")
            sel = Selector(text=html_str)
            item["description"] = " ".join(sel.xpath("//text()").getall())

        yield item
