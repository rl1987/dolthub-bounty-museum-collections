import scrapy

from urllib.parse import urlencode, urlparse, parse_qsl

PER_PAGE = 48

class DigitaltmuseumSpider(scrapy.Spider):
    name = 'digitaltmuseum'
    allowed_domains = ['digitaltmuseum.org']
    start_urls = ['https://digitaltmuseum.org/owners/']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_owner_list)

    def parse_owner_list(self, response):
        for l in response.xpath('//a[@class="module__grid"]/@href').getall():
            yield response.follow(l, callback=self.parse_owner_page)

    def parse_owner_page(self, response):
        museum_name = response.xpath('//meta[@name="og:description"]/@content').get()
        latitude = response.xpath('//figure[@class="c-owner-map"]/@lat').get()
        longitude = response.xpath('//figure[@class="c-owner-map"]/@lng').get()

        meta_dict = {
            'institution_name': museum_name,
            'latitude': latitude,
            'longitude': longitude
        }

        owner_abbrev = response.url.split("/")[-1]

        search_link = 'https://digitaltmuseum.org/search/?aq=owner%3A%22{}%22'.format(owner_abbrev)
        yield response.follow(search_link, callback=self.parse_search_page, meta=meta_dict)

    def parse_search_page(self, response):
        meta_dict = {
            'institution_name': response.meta.get('institution_name'),
            'latitude': response.meta.get('latitude'),
            'longitude': response.meta.get('longitude')
        }

        got_results = 0

        for l in response.xpath('//a[@class="module__grid"]/@href').getall():
            if l.startswith("/owner") or l.startswith("/search"):
                continue
            
            got_results += 1
            yield response.follow(l, callback=self.parse_object_page, meta=meta_dict)

        o = urlparse(response.url)
        old_params = dict(parse_qsl(o.query))

        params = dict(old_params)

        if old_params.get('o') is None:
            params['o'] = got_results
            params['n'] = PER_PAGE
            params['omit'] = 1
        else:
            if got_results < PER_PAGE:
                return

            params['o'] = int(old_params['o']) + PER_PAGE

        next_page_url = 'https://digitaltmuseum.org/search/?' + urlencode(params)
        yield scrapy.Request(next_page_url, self.parse_search_page, meta=meta_dict)

    def parse_object_page(self, response):
        pass

