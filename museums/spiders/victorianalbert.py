import scrapy

import json
from urllib.parse import urlparse, urlencode, parse_qsl

from museums.items import ObjectItem

# https://collections.vam.ac.uk/search/?page=1&page_size=15

class VictoriaNAlbertSpider(scrapy.Spider):
    name = 'victorianalbert'
    allowed_domains = ['api.vam.ac.uk', 'collections.vam.ac.uk']

    def start_requests(self):
        params = {
            "page": 1,
            "page_size": 50
        }

        url = "https://api.vam.ac.uk/v2/objects/search?" + urlencode(params)

        yield scrapy.Request(url, callback=self.parse_search_page)

    def recursively_generate_requests(self, clusters, params):
        n_cluster_keys = len(clusters)

        key = list(clusters.keys())[0]
        
        if n_cluster_keys == 1:
            for value in clusters.get(key):
                new_params = dict(params)
                new_params[key] = value

                url = "https://api.vam.ac.uk/v2/objects/search?" + urlencode(new_params)
                yield scrapy.Request(url, callback=self.parse_search_page)
        else:
            new_clusters = dict(clusters)
            del new_clusters[key]

            for value in clusters.get(key):
                new_params = dict(params)
                new_params[key] = value

                for request in self.recursively_generate_requests(new_clusters, new_params):
                    yield request

    def parse_clusters(self, response):
        json_dict = json.loads(response.text)

        clusters = dict()

        for cname, cdict in json_dict.get("clusters").items():
            clusters["id_" + cname] = list(map(lambda term: term.get("id"), cdict.get("terms")))

        self.logger.debug(clusters)
 
        params = {
            "page": 1,
            "page_size": 50
        }

        for request in self.recursively_generate_requests(clusters, params):
            self.logger.info(request)

    def parse_search_page(self, response):
        json_dict = json.loads(response.text)
        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))

        records = json_dict.get("records", [])
        for record in records:
            url = 'https://collections.vam.ac.uk/item/' + record.get("systemNumber")
            yield scrapy.Request(url, callback=self.parse_object_page)

        if len(records) < int(old_params.get('page_size')):
            return

        new_params = dict(old_params)
        new_params['page'] = int(new_params['page']) + 1
        
        url = "https://api.vam.ac.uk/v2/objects/search?" + urlencode(new_params)
        yield scrapy.Request(url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        item = ObjectItem()
    
        item['object_number'] = response.xpath('//meta[@property="og:url"]/@content').get().replace('/item/', '').replace('/', '')
        item['institution_name'] = 'Victoria and Albert Museum'
        item['institution_city'] = 'London'
        item['institution_state'] = 'England'
        item['institution_country'] = 'United Kingdom'
        item['institution_latitude'] = 51.494720458984375
        item['institution_longitude'] = -0.1917800009250641
        item['category'] = response.xpath('//a[@data-tracking-collections="tag - category"]/div/text()').get()
        item['title'] = response.xpath('//h1[@class="object-page__title"]/text()').get()
        # XXX: current_location
        item['dimensions'] = "|".join(response.xpath('//tr[./td[text()="Dimensions"]]//li/text()').getall())
        item['inscription'] = "|".join(response.xpath('//tr[./td[text()="Marks and Inscriptions"]]//li/text()').getall())
        item['provenance'] = response.xpath('//tr[./td[text()="Object history"]]//div[@class="etc-details__cell-free-content"]/text()').get()
        item['technique'] = "|".join(response.xpath('//a[@data-tracking-collections="tag - material"]/div/text()').getall())
        item['from_location'] = "|".join(response.xpath('//a[@data-tracking-collections="tag - place"]/div/text()').getall())
        # XXX: date_description, year_start, year end

        makers = response.xpath('//tr[./td[text()="Artist/Maker"]]//div[@class="etc-details__controlled-vocab-content"]/text()').getall()

        maker_names = []
        maker_roles = []

        for m in makers:
            maker_names.append(m.split(" (")[0])
            maker_roles.append(m.split(" (")[-1].replace(")", ""))

        item['maker_full_name'] = "|".join(maker_names)
        item['maker_role'] = "|".join(maker_roles)
        item['accession_number'] = response.xpath('//tr[./td[text()="Accession Number"]]//div/text()').get()
        item['credit_line'] = response.xpath('//tr[./td[text()="Credit line"]]//div/text()').get()
        item['image_url'] = response.xpath('//img[@class="object-page__hero-img"]/@src').get()
        item['source_1'] = response.url

        yield item

