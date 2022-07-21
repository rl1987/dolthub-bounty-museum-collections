import scrapy

import json
import logging

from scrapy.selector import Selector
from scrapy.http import FormRequest

from urllib.parse import urlencode, urlparse
from museums.items import ObjectItem

class CentrepompidouSpider(scrapy.Spider):
    name = 'centrepompidou'
    allowed_domains = ['www.centrepompidou.fr']
    start_urls = ['http://www.centrepompidou.fr/']

    def start_requests(self):
        params = {
            'tx__[action]': 'ajaxSearch',
            'tx__[controller]': 'Recherche',
            'type': '7891012',
            'cHash': '00c2bdba7f2587e76c56cfc79343dc63',
        }

        data = {
            'resultsType': 'arts',
            'displayType': 'Grid',
            'terms': '',
            'page': '1',
            'sort': 'default',
        }

        logging.info(data)

        url = "https://www.centrepompidou.fr/en/recherche?" + urlencode(params)

        yield FormRequest(url, formdata=data, callback=self.parse_search_page, meta={'formdata': data})
    
    def parse_search_page(self, response):
        form_data = response.meta.get('formdata')
        form_data['page'] = str(int(form_data['page']) + 1)

        logging.info(form_data)

        json_str = response.text
        json_dict = json.loads(json_str)

        html_str = json_dict.get("resultsList")

        sel = Selector(text=html_str)

        for l in sel.xpath('//a/@href').getall():
            yield response.follow(l, callback=self.parse_object_page)

        yield FormRequest(response.url, formdata=form_data, callback=self.parse_search_page, meta={'formdata': form_data})

    def parse_object_page(self, response):
        item = ObjectItem()

        item['object_number'] = response.xpath('//tr[./th[contains(text(), "Inventory no.")]]/td/text()').get("").strip()
        item['institution_name'] = 'Centre Pompidou'
        item['institution_city'] = 'Paris'
        item['institution_state'] = 'Île-de-France'
        item['institution_country'] = 'France'
        item['institution_latitude'] = 48.8608975
        item['institution_longitude'] = 2.3495319
        item['department'] = response.xpath('//tr[./th[contains(text(), "Collection area")]]/td/p/text()').get()
        item['category'] = "|".join(response.xpath('//table[@class="table"]//tr[./th[contains(text(), "Domain")]]/td/a/text()').getall())
        item['title'] = response.xpath('//h1/text()').get("").strip()
        item['dimensions'] =  response.xpath('//tr[./th[contains(text(), "Dimensions")]]/td/p/text()').get()
        item['inscription'] = " ".join(response.xpath('//tr[./th[contains(text(), "Inscriptions")]]/td/p/text()').getall())
        item['provenance'] = response.xpath('//tr[./th[contains(text(), "Notes")]]/td/p/text()').get()
        item['technique'] = response.xpath('//tr[./th[contains(text(), "Techniques")]]/td/p/text()').get()
        item['date_description'] = response.xpath('//p[@class="concept-date"]/text()').get()
        maker_names = response.xpath('//p[@class="concept-authors"]/a/text()').getall()
        maker_names = list(map(lambda m: m.strip(), maker_names))
        maker_names = "|".join(maker_names)
        item['maker_full_name'] = maker_names
        item['acquired_from'] = response.xpath('//tr[./th[contains(text(), "Acquisition")]]/td/p/text()').get()
        item['image_url'] = response.xpath('//meta[@property="og:image"]/@content').get()
        item['source_1'] = response.url

        yield item

