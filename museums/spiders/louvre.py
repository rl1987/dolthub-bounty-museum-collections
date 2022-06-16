import scrapy

from urllib.parse import urlencode, urlparse, parse_qsl, urljoin

from museums.items import ObjectItem

class LouvreSpider(scrapy.Spider):
    name = 'louvre'
    allowed_domains = ['louvre.fr']
    start_urls = ['https://collections.louvre.fr/en/recherche?page=1&limit=100']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

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
        item['description'] = ''.join(response.xpath('//div[./div[text()="Description/Features"]]/div[last()]/text()').getall()).strip()
        item['current_location'] = ' '.join(response.xpath('//div[./div[text()="Current location"]]/div[last()]/div/text()').getall()).strip()
        try:
            item['dimensions'] = response.xpath('//div[./div[text()="Dimensions"]]/div[last()]/text()').get().strip()
        except:
            pass

        item['inscription'] = ' '.join(response.xpath('//div[./div[text()="Inscriptions"]]/div[last()]/text()').getall()).strip()
        item['provenance'] = ' '.join(response.xpath('//div[./div[text()="Object history"]]/div[last()]/text()').getall()).strip() # XXX: is this correct?

        try:
            item['materials'] = response.xpath('//div[./div[text()="Materials and techniques"]]/div[last()]/text()').get().strip()
        except:
            pass

        item['technique'] = ' - '.join(response.xpath('//div[./div[text()="Techniques"]]/div[last()]/a/text()').getall()).strip()
        # XXX: from_location
        # XXX: culture
        item['date_description'] = response.xpath('//div[./div[text()="Date"]]/div[last()]/text()').get()
        # XXX: year_from
        # XXX: year_to
        item['maker_full_name'] = response.xpath('//div[./div[text()="Artist/maker / School / Artistic centre"]]/div[last()]/a[1]/text()').get()
        # XXX: maker_first_name, maker_last_name, maker_birth_year, maker_death_year, maker_role, maker_gender
        try:
            item['acquired_year'] = response.xpath('//div[./div[text()="Acquisition date"]]/div[last()]/text()').get().strip()
        except:
            pass

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
        item['source_2'] = response.xpath('//span[contains(text(), "JSON Record")]/a/@href').get()

        yield item
