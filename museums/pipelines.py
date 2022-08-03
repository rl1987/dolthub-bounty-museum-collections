# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import asyncio
import json
from urllib.parse import urlencode

from museums.settings import (
    TWILIO_ACCOUNT_SID,
    TWILIO_API_TOKEN,
    FROM_PHONE_NUMBER,
    TO_PHONE_NUMBER,
    GOOGLE_API_KEY,
)

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import scrapy

from twilio.rest import Client


class ConstraintEnforcementPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        object_number = adapter.get("object_number")
        if object_number is None or len(object_number) == 0:
            raise DropItem(
                "Constraint violation on item {}: empty object_number".format(
                    object_number
                )
            )

        if len(object_number) > 50:
            adapter["object_number"] = object_number[:50]

        institution_name = adapter.get("institution_name")
        if institution_name is None or len(institution_name) == 0:
            raise DropItem(
                "Constraint violation on item {}: empty institution_name".format(
                    institution_name
                )
            )

        institution_city = adapter.get("institution_city")
        if type(institution_city) == str and len(institution_city) > 500:
            adapter["institution_city"] = institution_city[:500]

        institution_state = adapter.get("institution_state")
        if type(institution_state) == str and len(institution_state) > 500:
            adapter["institution_state"] = institution_state[:500]

        institution_country = adapter.get("institution_country")
        if type(institution_country) == str and len(institution_country) > 500:
            adapter["institution_country"] = institution_country[:500]

        institution_latitude = adapter.get("institution_latitude")
        if institution_latitude is not None and type(institution_latitude) != float:
            try:
                adapter["institution_latitude"] = float(institution_latitude)
            except:
                raise DropItem(
                    "Constraint violation on item {}: institution_latitude cannot be converted to float".format(
                        item
                    )
                )

        institution_longitude = adapter.get("institution_longitude")
        if institution_longitude is not None and type(institution_longitude) != float:
            try:
                adapter["institution_longitude"] = float(institution_longitude)
            except:
                raise DropItem(
                    "Constraint violation on item {}: institution_longitude cannot be converted to float".format(
                        item
                    )
                )

        department = adapter.get("department")
        if type(department) == str and len(department) > 1000:
            adapter["department"] = department[:500]

        category = adapter.get("category")
        if type(category) == str and len(category) > 300:
            adapter["category"] = category[:300]

        title = adapter.get("title")
        if type(title) == str and len(title) > 1000:
            adapter["title"] = title[:1000]

        description = adapter.get("description")
        if type(description) == str and len(description) > 10000:
            adapter["description"] = description[:10000]

        current_location = adapter.get("current_location")
        if type(current_location) == str and len(current_location) > 500:
            adapter["current_location"] = current_location[:500]

        dimensions = adapter.get("dimensions")
        if type(dimensions) == str and len(dimensions) > 5000:
            adapter["dimensions"] = dimensions[:5000]

        inscription = adapter.get("inscription")
        if type(inscription) == str and len(inscription) > 4000:
            adapter["inscription"] = inscription[:4000]

        provenance = adapter.get("provenance")
        if type(provenance) == str and len(provenance) > 4000:
            adapter["provenance"] = provenance[:4000]

        materials = adapter.get("materials")
        if type(materials) == str and len(materials) > 10000:
            adapter["materials"] = materials[:10000]

        technique = adapter.get("technique")
        if type(technique) == str and len(technique) > 200:
            adapter["technique"] = technique[:200]

        from_location = adapter.get("from_location")
        if type(from_location) == str and len(from_location) > 4000:
            adapter["from_location"] = from_location[:4000]

        culture = adapter.get("culture")
        if type(culture) == str and len(culture) > 2000:
            adapter["culture"] = culture[:2000]

        date_description = adapter.get("date_description")
        if type(date_description) == str and len(date_description) > 500:
            adapter["date_description"] = date_description[:500]

        year_start = adapter.get("year_start")
        if year_start is not None and type(year_start) != int:
            try:
                adapter["year_start"] = int(year_start)
            except:
                raise DropItem(
                    "Constraint violation on item {}: year_start cannot be converted to int".format(
                        item
                    )
                )

        year_end = adapter.get("year_end")
        if year_end is not None and type(year_end) != int:
            try:
                adapter["year_end"] = int(year_end)
            except:
                raise DropItem(
                    "Constraint violation on item {}: year_end cannot be converted to int".format(
                        item
                    )
                )

        maker_full_name = adapter.get("maker_full_name")
        if type(maker_full_name) == str and len(maker_full_name) > 3000:
            adapter["maker_full_name"] = maker_full_name[:3000]

        maker_first_name = adapter.get("maker_first_name")
        if type(maker_first_name) == str and len(maker_first_name) > 500:
            adapter["maker_first_name"] = maker_first_name[:500]

        maker_last_name = adapter.get("maker_last_name")
        if type(maker_last_name) == str and len(maker_last_name) > 500:
            adapter["maker_last_name"] = maker_last_name[:500]

        maker_birth_year = adapter.get("maker_birth_year")
        if type(maker_birth_year) == str and len(maker_birth_year) > 2000:
            adapter["maker_birth_year"] = maker_birth_year[:2000]

        maker_death_year = adapter.get("maker_death_year")
        if type(maker_death_year) == str and len(maker_death_year) > 2000:
            adapter["maker_death_year"] = maker_death_year[:2000]

        maker_role = adapter.get("maker_role")
        if type(maker_role) == str and len(maker_role) > 2000:
            adapter["maker_role"] = maker_role[:2000]

        maker_gender = adapter.get("maker_gender")
        if type(maker_gender) == str and len(maker_gender) > 500:
            adapter["maker_gender"] = maker_gender[:500]

        acquired_year = adapter.get("acquired_year")
        if acquired_year is not None and type(acquired_year) != int:
            try:
                adapter["acquired_year"] = int(acquired_year)
            except:
                raise DropItem(
                    "Constraint violation on item {}: acquired_year cannot be converted to int".format(
                        acquired_year
                    )
                )

        acquired_from = adapter.get("acquired_from")
        if type(acquired_from) == str and len(acquired_from) > 200:
            adapter["acquired_from"] = acquired_from[:200]

        accession_year = adapter.get("accession_year")
        if accession_year is not None and type(accession_year) != int:
            try:
                adapter["accession_year"] = int(accession_year)
            except:
                raise DropItem(
                    "Constraint violation on item {}: accession_year cannot be converted to int".format(
                        item
                    )
                )

        accession_year = adapter.get("accession_year")
        if type(accession_year) == str and len(accession_year) > 500:
            adapter["accession_year"] = accession_year[:500]

        credit_line = adapter.get("credit_line")
        if type(credit_line) == str and len(credit_line) > 4000:
            adapter["credit_line"] = credit_line[:4000]

        image_url = adapter.get("image_url")
        if (
            type(image_url) == str and len(image_url) > 2000
        ):  # XXX: maybe implement smarter truncation that would drop one or more URLs from the end of pipe-separated list
            adapter["image_url"] = image_url[:2000]

        source_1 = adapter.get("source_1")
        if source_1 is None or len(source_1) == 0:
            raise DropItem(
                "Constraint violation on item {}: source_1 cannot be empty".format(item)
            )

        if type(source_1) == str and len(source_1) > 2048:
            raise DropItem(
                "Constraint violation on item {}: source_1 cannot be longer than 2048 characters".format(
                    item
                )
            )

        source_2 = adapter.get("source_2")
        if type(source_2) == str and len(source_2) > 2048:
            del adapter["source_2"]

        return item


class NotificationPipeline:
    def close_spider(self, spider):
        msg = "Spider {} finished scraping.".format(spider.name)

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_API_TOKEN)
        message = client.messages.create(
            body=msg, from_=FROM_PHONE_NUMBER, to=TO_PHONE_NUMBER
        )

        spider.logger.info(message)


class InstitutionGeoEnrichmentPipeline:
    location_by_name = dict()
    place_by_name = dict()

    # https://developers.google.com/maps/documentation/geocoding/requests-reverse-geocoding
    async def reverse_geocode(self, spider, adapter):
        name = adapter.get("institution_name")
        latitude = adapter.get("institution_latitude")
        longitude = adapter.get("institution_longitude")

        if latitude is None or longitude is None:
            return

        if self.location_by_name.get(name) is None:
            params = {
                "latlng": "{},{}".format(latitude, longitude),
                "key": GOOGLE_API_KEY,
            }

            url = "https://maps.googleapis.com/maps/api/geocode/json?" + urlencode(
                params
            )

            request = scrapy.Request(url)
            response = await spider.crawler.engine.download(request, spider)

            json_dict = json.loads(response.text)

            self.location_by_name[name] = json_dict
        else:
            json_dict = self.location_by_name[name]

        results = json_dict.get("results", [])
        if len(results) > 0:
            result = results[0]

            for ac in result.get("address_components", []):
                types = ac.get("types")
                if "country" in types:
                    adapter["institution_country"] = ac.get("long_name")
                elif "locality" in types:
                    adapter["institution_city"] = ac.get("short_name")
                elif "administrative_area_level_1" in types:
                    adapter["institution_state"] = ac.get("short_name")

    # https://developers.google.com/maps/documentation/places/web-service/search-find-place
    async def find_place(self, spider, adapter):
        name = adapter.get("institution_name")
        if self.place_by_name.get(name) is None:
            query = name
            if adapter.get("institution_city") is not None:
                query += " " + adapter.get("institution_city")
            if adapter.get("institution_country") is not None:
                query += " " + adapter.get("institution_country")

            params = {
                "fields": "geometry",
                "key": GOOGLE_API_KEY,
                "input": query,
                "inputtype": "textquery",
            }

            url = (
                "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
                + urlencode(params)
            )
            request = scrapy.Request(url)

            response = await spider.crawler.engine.download(request, spider)

            json_dict = json.loads(response.text)

            self.place_by_name[name] = json_dict
        else:
            json_dict = self.place_by_name[name]

        results = json_dict.get("candidates", [])
        if len(results) == 0:
            raise DropItem("Cannot find {} on Google Maps API - dropping".format(name))

        result = results[0]

        geometry = result.get("geometry", dict())
        location = geometry.get("location", dict())

        adapter["institution_latitude"] = location.get("lat")
        adapter["institution_longitude"] = location.get("lng")

        await self.reverse_geocode(spider, adapter)

    async def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        city = adapter.get("institution_city")
        state = adapter.get("institution_state")
        country = adapter.get("institution_country")
        latitude = adapter.get("institution_latitude")
        longitude = adapter.get("institution_longitude")

        if not None in (city, state, country, latitude, longitude):
            return item

        if latitude is not None and longitude is not None:
            await self.reverse_geocode(spider, adapter)
        elif city is None or state is None or country is None:
            await self.find_place(spider, adapter)

        return item
