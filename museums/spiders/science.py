import scrapy

from urllib.parse import urlparse, urlencode, parse_qsl

class ScienceSpider(scrapy.Spider):
    name = 'science'
    allowed_domains = ['collection.sciencemuseumgroup.org.uk']
    start_urls = ['https://collection.sciencemuseumgroup.org.uk/search/objects?page[size]=100']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_categories)

    def parse_categories(self, response):
        for category in response.xpath('//div[@data-filter="Category"]//input/@value').getall():
            category = category.lower()
            category = category.replace(" ", "-")

            url = "https://collection.sciencemuseumgroup.org.uk/search/objects/categories/{}?page[size]=100".format(category)

            yield scrapy.Request(url, callback=self.parse_object_types)

    def parse_object_types(self, response):
        o = urlparse(response.url)
        params = dict(parse_qsl(o.query))
    
        for object_type in response.xpath('//div[@data-filter="Type"]//input/@value').getall():
            object_type = object_type.lower()
            object_type = object_type.replace(" ", "-")

            url = "https://collection.sciencemuseumgroup.org.uk" + o.path + "/object_type/" + object_type + "?" + urlencode(params)

            yield scrapy.Request(url, callback=self.parse_search_page)

    def parse_search_page(self, response):
        for object_url in response.xpath('//div[@class="searchresults__column"]/a/@href').getall():
            yield scrapy.Request(object_url, callback=self.parse_object_page)

        next_page_url = response.xpath('//li[@class="pagination-next"]/a/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        pass
