import scrapy
from scrapy.http import JsonRequest

import json
import logging

from museums.items import ObjectItem


class CarnegieSpider(scrapy.Spider):
    name = "carnegie"
    allowed_domains = [
        "collection.cmoa.org",
        "530828c83afb4338b9927d95f5792ed5.us-east-1.aws.found.io",
    ]
    start_urls = ["http://collection.cmoa.org/"]
    headers = {
        "authority": "530828c83afb4338b9927d95f5792ed5.us-east-1.aws.found.io:9243",
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "authorization": "Basic Y29sbGVjdGlvbnM6bzQxS0chTW1KUSRBNjY=",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://collection.cmoa.org",
        "pragma": "no-cache",
        "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    }

    def start_requests(self):
        json_dict = {
            "_source": ["id", "title", "creators", "creation_date", "images", "type"],
            "query": {"bool": {"must": [{"match_all": {}}], "filter": []}},
            "aggs": {
                "uniqueClassification": {
                    "terms": {
                        "field": "medium",
                        "order": {"_key": "asc"},
                        "shard_size": 2000,
                        "size": 500,
                    }
                },
                "uniqueDepartment": {
                    "terms": {
                        "field": "department",
                        "order": {"_key": "asc"},
                        "shard_size": 2000,
                        "size": 500,
                    }
                },
                "uniqueLocation": {
                    "terms": {
                        "field": "current_location",
                        "order": {"_key": "asc"},
                        "shard_size": 2000,
                        "size": 500,
                    }
                },
                "creators": {
                    "nested": {"path": "creators"},
                    "aggs": {
                        "uniqueCreator": {
                            "terms": {
                                "field": "creators.label",
                                "order": {"_count": "desc"},
                                "shard_size": 2000,
                                "size": 500,
                            },
                            "aggs": {
                                "cited": {
                                    "terms": {"field": "creators.cited_name"},
                                    "aggs": {
                                        "sort": {
                                            "terms": {
                                                "field": "creators.cited_name.sort"
                                            }
                                        }
                                    },
                                }
                            },
                        },
                        "uniqueNationality": {
                            "terms": {
                                "field": "creators.nationality",
                                "order": {"_key": "asc"},
                                "shard_size": 2000,
                                "size": 500,
                            }
                        },
                    },
                },
            },
            "post_filter": {"bool": {"filter": []}},
            "sort": [
                {
                    "creators.cited_name.sort": {
                        "order": "asc",
                        "nested": {"path": "creators"},
                    }
                }
            ],
        }

        logging.debug(json_dict)
        url = "https://530828c83afb4338b9927d95f5792ed5.us-east-1.aws.found.io:9243/cmoa_objects/_search?scroll=1m"

        yield JsonRequest(
            url,
            headers=self.headers,
            data=json_dict,
            callback=self.parse_search_api_response,
            meta={"dont_cache": True},
        )

    def parse_search_api_response(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)

        n = 0

        for hit_dict in json_dict.get("hits", dict()).get("hits", []):
            source_id = hit_dict.get("_id")
            url = "https://530828c83afb4338b9927d95f5792ed5.us-east-1.aws.found.io:9243/cmoa_objects/object/{}/_source".format(
                source_id.replace(":", "%3A").replace("/", "%2F")
            )
            n += 1
            yield scrapy.Request(
                url, headers=self.headers, callback=self.parse_source_api_response
            )

        if n == 0:
            return

        scroll_id = json_dict.get("_scroll_id")
        if scroll_id is None:
            return

        json_payload = {"scroll": "1m", "scroll_id": scroll_id}

        logging.debug(json_payload)

        # https://www.elastic.co/guide/en/elasticsearch/reference/5.4/search-request-scroll.html
        # https://stackoverflow.com/questions/46336470/elasticsearch-unknown-key-for-a-value-string-in-scroll
        # https://www.repost.aws/questions/QU9nXbumxSS9m64r3ZaoN_NA/how-to-perform-scroll-scroll-not-working-on-amazon-elasticsearch
        yield JsonRequest(
            "https://530828c83afb4338b9927d95f5792ed5.us-east-1.aws.found.io:9243/_search/scroll",
            headers=self.headers,
            data=json_payload,
            callback=self.parse_search_api_response,
            dont_filter=True,
            meta={"dont_cache": True},
        )

    def textify_measurements(self, measurements):
        if measurements is None or len(measurements) == 0:
            return None

        text = ""

        for submeasurement in measurements:
            m_type = submeasurement.get("type", "")
            if m_type is not None:
                text += m_type + ": "

            text += (
                submeasurement.get("fraction", dict()).get("height", "")
                + " x "
                + submeasurement.get("fraction", dict()).get("width", "")
            )
            if submeasurement.get("fraction", dict()).get("depth") is not None:
                text += " x " + submeasurement.get("fraction").get("depth")

            text += " in ("
            text += (
                submeasurement.get("decimal", dict()).get("width", "")
                + " x "
                + submeasurement.get("decimal", dict()).get("height", "")
            )
            if submeasurement.get("decimal", dict()).get("depth") is not None:
                text += " x " + submeasurement.get("decimal").get("depth")
            text += " cm)\n"

        return text

    def parse_source_api_response(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)

        item = ObjectItem()

        item["institution_name"] = "Carnegie Museum of Art"
        item["institution_city"] = "Pittsburgh"
        item["institution_state"] = "PA"
        item["institution_country"] = "United States"
        item["institution_latitude"] = 40.4437052
        item["institution_longitude"] = -79.9511614
        item["department"] = json_dict.get("department")
        item["category"] = json_dict.get("type")
        item["title"] = json_dict.get("title")
        # XXX: description
        item["current_location"] = json_dict.get("current_location")
        item["dimensions"] = self.textify_measurements(json_dict.get("measurements"))
        # XXX: inscription, provenance
        item["materials"] = json_dict.get("medium")
        item["technique"] = json_dict.get("medium_description")
        item["from_location"] = json_dict.get("creation_address")
        item["date_description"] = json_dict.get("creation_date")[0]

        try:
            item["year_start"] = int(json_dict.get("creation_date")[0])
            item["year_end"] = int(json_dict.get("creation_date")[-1])
        except:
            pass

        makers = json_dict.get("creators", [])
        if makers is not None and len(makers) > 0:
            maker_names = list(map(lambda m: m.get("label"), makers))
            maker_birth_years = list(map(lambda m: str(m.get("birth", "")), makers))
            maker_death_years = list(map(lambda m: str(m.get("death", "")), makers))
            maker_genders = list(map(lambda m: str(m.get("gender")), makers))

            item["maker_full_name"] = "|".join(maker_names)
            item["maker_birth_year"] = "|".join(maker_birth_years).replace("None", "")
            item["maker_death_year"] = "|".join(maker_death_years).replace("None", "")
            item["maker_gender"] = "|".join(maker_genders).replace("None", "")

        try:
            item["acquired_year"] = json_dict.get("acquisition_date", "").split("-")[0]
        except:
            pass

        item["acquired_from"] = json_dict.get("acquisition_method")
        item["object_number"] = json_dict.get("accession_number")
        item["accession_number"] = json_dict.get("accession_number")
        item["credit_line"] = json_dict.get("credit_line")

        if len(json_dict.get("images", [])) > 0:
            filename = json_dict.get("images")[0].get("filename")
            irn = json_dict.get("images")[0].get("irn")
            item[
                "image_url"
            ] = "https://cmoa-collection-images.s3.amazonaws.com/{}/{}/{}".format(
                item["category"], irn, filename
            )

        item["source_1"] = "https://collection.cmoa.org/objects/" + item[
            "object_number"
        ].replace("cmoa:objects/", "")
        item["source_2"] = response.url

        yield item
