import scrapy

from urllib.parse import urlparse, parse_qsl, urlencode
import json

from museums.items import ObjectItem


class MamparisSpider(scrapy.Spider):
    name = "mamparis"
    allowed_domains = ["mam.paris.fr", "api.navigart.fr"]
    start_urls = ["http://mam.paris.fr/"]

    def start_requests(self):
        params = {"sort": "by_author", "size": 60, "from": 0}

        url = "https://api.navigart.fr/18/artworks?" + urlencode(params)

        yield scrapy.Request(url, callback=self.parse_search_results)

    def get_image_urls(self, medias):
        if medias is None:
            return []

        image_urls = []

        for media in medias:
            url_template = media.get("url_template")

            max_width = 1000  # XXX: is this right?
            file_name = media.get("file_name")

            url = url_template.replace("{size}", str(max_width)).replace(
                "{file_name}", file_name
            )

            image_urls.append(url)

        return image_urls

    def parse_search_results(self, response):
        json_dict = json.loads(response.text)

        results = json_dict.get("results")
        if results is None or len(results) == 0:
            return

        for result_dict in results:
            result_dict = result_dict.get("_source", dict()).get("ua")
            artwork_dict = result_dict.get("artwork")
            authors = result_dict.get("authors", [])
            medias = result_dict.get("medias", [])

            item = ObjectItem()

            item["object_number"] = artwork_dict.get("_id")

            item["institution_name"] = "Musée National d'Art Moderne"
            item["institution_city"] = "Paris"
            item["institution_state"] = "Île-de-France"
            item["institution_country"] = "France"
            item["institution_latitude"] = 40.761509
            item["institution_longitude"] = -73.978271

            item["department"] = artwork_dict.get("collection_department_label_case")
            item["category"] = artwork_dict.get("domain")
            item["title"] = artwork_dict.get("title_notice")
            item["description"] = artwork_dict.get("comments")
            # XXX: current_location
            item["dimensions"] = artwork_dict.get("dimensions")
            item["inscription"] = artwork_dict.get("inscriptions")
            # XXX: provenance, materials, technique, from_location, culture
            item["date_description"] = artwork_dict.get("date_creation")
            # XXX: year_start, year_end

            maker_full_name = list(
                map(lambda a: a.get("name", dict()).get("notice2"), authors)
            )
            maker_full_name = "|".join(maker_full_name)
            item["maker_full_name"] = maker_full_name

            # XXX: maker_birth_year, maker_death_year

            try:
                maker_role = list(map(lambda a: a.get("type"), authors))
                maker_role = "|".join(maker_role)
                item["maker_role"] = maker_role
            except:
                pass

            try:
                maker_gender = list(map(lambda a: a.get("gender"), authors))
                maker_gender = "|".join(maker_gender)
                item["maker_gender"] = maker_gender
            except:
                pass

            item["acquired_year"] = artwork_dict.get("acquisition_year")
            if type(item["acquired_year"]) == float or (
                type(item["acquired_year"]) == str and "." in item["acquired_year"]
            ):
                item["acquired_year"] = int(item["acquired_year"])

            item["acquired_from"] = artwork_dict.get("acquisition_mode")
            item["image_url"] = "|".join(self.get_image_urls(medias))

            item["source_1"] = (
                "https://www.mam.paris.fr/fr/collections-en-ligne#/artwork/"
                + item["object_number"]
            )
            item["source_2"] = (
                "https://api.navigart.fr/18/artworks/" + item["object_number"]
            )

            yield item

        if len(results) < 60:
            return

        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))

        new_params = dict(old_params)

        new_params["from"] = int(new_params["from"]) + 60

        url = "https://api.navigart.fr/18/artworks?" + urlencode(new_params)

        yield scrapy.Request(url, callback=self.parse_search_results)
