import scrapy
from scrapy.selector import Selector

import json
from urllib.parse import urlparse, urlencode, parse_qsl

from museums.items import ObjectItem

class MucemSpider(scrapy.Spider):
    name = 'mucem'
    allowed_domains = ['www.mucem.org']
    start_urls = ['https://www.mucem.org/en/collections/explorez-les-collections/next-page?term=a&page=1']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        json_str = response.text
        json_dict = json.loads(json_str)
        html_str = json_dict.get("html")

        sel = Selector(text=html_str)

        for url in sel.xpath('//a/@href').getall():
            yield scrapy.Request(url, callback=self.parse_object_page)

        is_next_page = json_dict.get("next_button", False)
        if is_next_page:
            o = urlparse(response.url)
            params = dict(parse_qsl(o.query))
            params['page'] = int(params['page']) + 1

            next_page_url = 'https://www.mucem.org/en/collections/explorez-les-collections/next-page?' + urlencode(params)

            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        item = ObjectItem()

        item['object_number'] = response.xpath('//div[./label[text()="Numero d\'inventaire :"]]/div[@class="detail_objet"]/p/text()').get()
        item['institution_name'] = 'The Mucem'
        item['institution_city'] = 'Marseille'
        item['institution_state'] = 'Provence-Alpes-Côte d\'Azur'
        item['institution_country'] = 'France'
        item['institution_latitude'] = 43.2966941
        item['institution_longitude'] = 5.3588938
        item['title'] = response.xpath('//h1/text()').get()
        item['description'] = " ".join(response.xpath('//div[./label[text()="Description :"]]//p/text()').getall())
        item['dimensions'] = "|".join(response.xpath('//div[./label[text()="Dimensions et poids :"]]//p/text()').getall())
        item['materials'] = "|".join(response.xpath('//div[./label[text()="Materials & techniques :"]]//p/text()').getall())
        item['from_location'] = response.xpath('//label[@class="lieu" and text()="Emplacement :"]/following-sibling::div/p/text()').get()
        item['date_description'] = response.xpath('//label[@class="date" and text()="Date :"]/following-sibling::div/p/text()').get()
        item['maker_full_name'] = response.xpath('//label[@class="prenom" and text()="Author / Performer :"]/following-sibling::div/p/span/text()').get("").strip()
        item['image_url'] = response.xpath('//meta[@property="og:image"]/@content').get()
        item['source_1'] = response.url

        yield item

