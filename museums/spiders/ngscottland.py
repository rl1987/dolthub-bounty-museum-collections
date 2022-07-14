import scrapy


class NgscottlandSpider(scrapy.Spider):
    name = 'ngscottland'
    allowed_domains = ['nationalgalleries.org']
    start_urls = ['https://www.nationalgalleries.org/search?sort=title&page=0']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        links = response.xpath('//h2/a[contains(@class, "ngs-search-result__link")]/@href').getall()
        for l in links:
            yield response.follow(l, callback=self.parse_artwork_page)
        
        next_page_link = response.xpath('//a[contains(@class, "ngs-pagination__link--next")]/@href').get()
        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse_search_page)

    def parse_artwork_page(self, response):
        pass

