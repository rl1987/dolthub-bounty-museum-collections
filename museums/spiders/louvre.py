import scrapy

from urllib.parse import urlencode, urlparse, parse_qsl, urljoin

class LouvreSpider(scrapy.Spider):
    name = 'louvre'
    allowed_domains = ['louvre.fr']
    #start_urls = ['https://collections.louvre.fr/en/recherche?page=1&limit=100']
    start_urls = ['https://collections.louvre.fr/en/recherche?page=1&limit=100&location%5B0%5D=147894']

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
        pass
