import scrapy
from scrapy.selector import Selector

import json
from urllib.parse import urlparse, parse_qsl, urlencode

from museums.items import ObjectItem

class BranlySpider(scrapy.Spider):
    name = 'branly'
    allowed_domains = ['www.quaibranly.fr']
    start_urls = ['https://www.quaibranly.fr/fr/explorer-les-collections/base/Work/action/list/?format=json&search=true&category=oeuvres&page=1&mode=thumb&orderby=null&order=desc&category=oeuvres&tx_mqbcollection_explorer%5Bquery%5D%5Btype%5D=&tx_mqbcollection_explorer%5Bquery%5D%5Bclassification%5D=&tx_mqbcollection_explorer%5Bquery%5D%5Bexemplaire%5D=']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)
        html_str = json_dict.get("html")

        sel = Selector(text=html_str)

        for link in sel.xpath('//figure/a/@href').getall():
            yield response.follow(link, callback=self.parse_object_page)

        total_pages = json_dict.get("nbPages")

        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))

        params = dict(old_params)
        page = int(params['page'])

        if page <= total_pages:
            page += 1
            params['page'] = page

            next_page_url = 'https://www.quaibranly.fr/fr/explorer-les-collections/base/Work/action/list/?' + urlencode(params)
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        item = ObjectItem()

        item['object_number'] = "".join(response.xpath('//li[@class="description-item" and ./b[text()="Numéro de gestion :"]]/text()').getall()).strip()
        item['institution_name'] = 'Musée du quai Branly'
        item['institution_city'] = 'Paris'
        item['institution_state'] = 'Île-de-France'
        item['institution_country'] = 'France'
        item['institution_latitude'] = 48.8609242
        item['institution_longitude'] = 2.2968265
        # XXX: department
        item['category'] = " ".join(response.xpath('//li[@class="description-item" and ./b[text()="Type d\'objet :"]]/text()').getall()).strip()
        item['title'] = response.xpath('//div[@class="intro"]/h1/text()').get()
        item['description'] = response.xpath('//div[@class="edito"]/p[@class="more"]/text()').get("").strip()
        item['current_location'] = " ".join(response.xpath('//li[@class="description-item" and ./b[text()="Exposé :"]]/text()').getall()).strip()
        item['dimensions'] = " ".join(response.xpath('//li[@class="description-item" and ./b[text()="Dimensions et poids :"]]/text()').getall()).strip()
        # XXX: inscription, provenance
        item['materials'] = " ".join(response.xpath('//li[@class="description-item" and ./b[text()="Matériaux et techniques :"]]/text()').getall()).strip()
        item['from_location'] = response.xpath('//li[@class="description-item" and ./b[text()="Donateur : "]]/a/text()').get("").strip()
        cultures = response.xpath('//li[@class="description-item" and ./b[text()="Culture : "]]/a/text()').getall()
        cultures = list(map(lambda c: c.strip(), cultures))
        cultures = "|".join(cultures)
        item['culture'] = cultures
        item['date_description'] = " ".join(response.xpath('//li[@class="description-item" and ./b[text()="Date :"]]/text()').getall()).strip()
        item['maker_full_name'] = response.xpath('//li[@class="description-item" and ./b[text()="Photographe : " or text()="Dessinateur : "]]/a/text()').get("").strip() # XXX: improve to cover more types of makers
        # XXX: maker_role
        item['acquired_from'] = response.xpath('//li[@class="description-item" and ./b[text()="Donateur : "]]/a/text()').get("").strip()
        item['accession_number'] = "".join(response.xpath('//li[@class="description-item" and ./b[text()="Numéro d\'inventaire :"]]/text()').getall()).strip()
        item['image_url'] = response.xpath('//li/@data-zoom').get()
        item['source_1'] = response.url

        if item['object_number'] == '':
            item['object_number'] = item['accession_number']

        yield item

