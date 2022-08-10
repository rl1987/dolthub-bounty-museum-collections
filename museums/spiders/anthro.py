import scrapy
from scrapy.http import FormRequest

import logging

import js2xml
from aroay_cloudscraper import CloudScraperRequest

PER_PAGE = 20

class AnthroSpider(scrapy.Spider):
    name = 'anthro'
    allowed_domains = ['anthro.amnh.org']
    start_urls = ['https://anthro.amnh.org/anthropology/databases/common/query_result.cfm',
            "https://anthro.amnh.org/anthropology/databases/common/query_categories.cfm?"]

    def start_requests(self):
        yield CloudScraperRequest(self.start_urls[-1], callback=self.parse_categories, headers={'Referer': 'https://anthro.amnh.org/collections'})

    def parse_categories(self, response):
        print(response.text)
        for coll_id in response.xpath('//select[@name="coll_id"]/option/@value').getall():
            if coll_id == "-ALL-":
                continue

            form_data = {
                'object_list': '',
                'search_list': 'nm',
                'coll_id' : str(coll_id),
                'type_base': '-ALL-',
                'country_list': '-ALL-',
                'culture_list': '-ALL-',
                'categories': '',
                'current_view': 'fm',
                'imaged': '',
                'rec_per_page': str(PER_PAGE)
            }

            logging.debug(form_data)

            yield scrapy.FormRequest(self.start_urls[0], formdata=form_data, callback=self.parse_object_list)

    def parse_object_list(self, response):
        object_links =  response.xpath('//a[@target="DetailPage"]/@href').getall()
        
        for l in object_links:
            yield response.follow(l, callback=self.parse_object_page)

        # onclick="nextMove(3,1,20,60082);document.forms[0].set_selection.value=document.forms[0].set_selection_IE.value; document.forms[0].save_page.value='no'; document.HiddenForm1.target='_self'; document.forms[0].submit(); return false"

        next_page_link_sel = response.xpath('//a[./img[@name="next"]]')
        onclick = next_page_link_sel.attrib.get('onclick')
        parsed = j2xml.parse(onclick)
        args = parsed.xpath('//functioncall[1]//number/@value')
        
        form_data = dict()

        for input_sel in response.xpath('//input[@type="hidden"]'):
            name = input_sel.attrib.get("name")
            value = input_sel.attrib.get("value")

        form_data['current_record'] = int(args[1]) + int(args[2])
        form_data['set_selection_IE'] = 'no'
        form_data['save_page'] = 'no'
        form_data['set_selection'] = 'no'

        logging.debug(form_data)

        yield scrapy.FormRequest(self.start_urls[0], formdata=form_data, callback=self.parse_object_list)

    def parse_object_page(self, response):
        pass
