import scrapy

import json
from urllib.parse import urlencode, urlparse, parse_qsl, urljoin

from museums.items import ObjectItem

class LouvreSpider(scrapy.Spider):
    name = 'louvre'
    allowed_domains = ['louvre.fr']
    start_urls = ['https://collections.louvre.fr/en/recherche?page=1&limit=100']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def _get_maker_birth_year(self, creator_dict):
        for date_dict in creator_dict.get("dates", []):
            if date_dict.get("type") == "date 1" or date_dict.get("type") == "date de naissance":
                return date_dict.get("date")

        return ""

    def _get_maker_death_year(self, creator_dict):
        for date_dict in creator_dict.get("dates", []):
            if date_dict.get("type") == "date 2" or date_dict.get("type") == "date de mort":
                return date_dict.get("date")

        return ""

    def parse_search_page(self, response):
        for artwork_link in response.xpath('//div[@class="card__outer"]//a/@href').getall():
            artwork_url = urljoin(response.url, artwork_link)
            yield scrapy.Request(artwork_url, callback=self.parse_artwork_page)

        if response.xpath('//button[@aria-label="Show next page" and not(contains(@class, "inactive"))]') is None:
            return
        
        o = urlparse(response.url)
        
        old_params = parse_qsl(o.query)
        old_params = dict(old_params)

        new_params = dict(old_params)
        new_params['page'] = int(old_params['page']) + 1

        new_url = response.url.split("?")[0] + "?" + urlencode(new_params)

        yield scrapy.Request(new_url, callback=self.parse_search_page)

    def parse_artwork_page(self, response):
        item = ObjectItem()

        item['object_number'] = ''.join(response.xpath('//div[./div[text()="Inventory number"]]/div[last()]/text()').getall()).strip()
        item['institution_name'] = 'Louvre Museum'
        item['institution_city'] = 'Paris'
        item['institution_state'] = 'Île-de-France'
        item['institution_country'] = 'France'
        item['institution_latitude'] = 48.860294
        item['institution_longitude'] = 2.338629
        item['department'] = response.xpath('//div[./div[text()="Collection"]]/div[last()]/a/text()').get()
        item['category'] = response.xpath('//div[./div[text()="Category"]]/div[last()]/a/text()').get()
        item['title'] = response.xpath('//h1[@class="notice__title h_1"]/text()').get()
        item['description'] = ''.join(response.xpath('//div[./h2[text()="Description"]]//div[./div[text()="Description/Features"]]/div[last()]/text()').getall()).strip()
        item['current_location'] = ' '.join(response.xpath('//div[./div[text()="Current location"]]/div[last()]/div/text()').getall()).strip()
        try:
            item['dimensions'] = response.xpath('//div[./div[text()="Dimensions"]]/div[last()]/text()').get().strip()
        except:
            pass

        item['inscription'] = ' '.join(response.xpath('//div[./div[text()="Inscriptions"]]/div[last()]/text()').getall()).strip()
        item['provenance'] = ' '.join(response.xpath('//div[./div[text()="Object history"]]/div[last()]/text()').getall()).strip() # XXX: is this correct?

        item['materials'] = ' - '.join(response.xpath('//div[./div[text()="Materials"]]/div[last()]/a/text()').getall()).strip()
        item['technique'] = ' - '.join(response.xpath('//div[./div[text()="Techniques"]]/div[last()]/a/text()').getall()).strip()
        # XXX: from_location
        # XXX: culture
        item['date_description'] = response.xpath('//div[./div[text()="Date"]]/div[last()]/text()').get()

        item['maker_full_name'] = response.xpath('//div[./div[text()="Artist/maker / School / Artistic centre"]]/div[last()]/a[1]/text()').get()
        # XXX: maker_first_name, maker_last_name, maker_birth_year, maker_death_year, maker_role, maker_gender

        try:
            item['acquired_from'] = response.xpath('//div[./div[text()="Collector / Previous owner / Commissioner / Archaeologist / Dedicatee"]]/div[last()]/text()').get().strip() # XXX: sometimes there's links in this
        except:
            pass

        # XXX: accession_year, accession_number

        try:
            item['image_url'] = response.xpath('//picture//img/@data-full-src').get()
            item['image_url'] = urljoin(response.url, item['image_url'])
        except:
            pass

        item['source_1'] = response.url
        item['source_2'] = response.xpath('//span[contains(text(), "JSON Record")]/a/@href').get() # TODO: consider also parsing the JSON file

        yield scrapy.Request(item['source_2'], callback=self.parse_artwork_json, meta={'item':item})

    def parse_artwork_json(self, response):
        item = response.meta.get('item')

        json_dict = json.loads(response.text)

        item['object_number'] = json_dict.get("arkId")

        if json_dict.get("acquisitionDetails") is not None and len(json_dict.get("acquisitionDetails")) > 0:
            try:
                item['acquired_year'] = json_dict.get('acquisitionDetails')[-1].get('dates')[-1].get('startYear')
            except:
                pass

        creators = json_dict.get("creator")
        if creators is not None and len(creators) > 0:
            maker_full_names = list(map(lambda c: c.get("label"), creators))
            maker_full_names = "|".join(maker_full_names)
            item['maker_full_name'] = maker_full_names

            maker_roles = list(map(lambda c: c.get("creatorRole"), creators))
            maker_roles = "|".join(maker_roles)
            item['maker_role'] = maker_roles

            maker_birth_years = list(map(lambda c: self._get_maker_birth_year(c), creators))
            maker_birth_years = "|".join(maker_birth_years)
            item['maker_birth_year'] = maker_birth_years

            maker_death_years = list(map(lambda c: self._get_maker_death_year(c), creators))
            maker_death_years = "|".join(maker_death_years)
            item['maker_death_year'] = maker_death_years
    
        item['provenance'] = json_dict.get("provenance")

        yield item


