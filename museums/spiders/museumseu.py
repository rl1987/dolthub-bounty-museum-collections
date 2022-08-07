import scrapy

from urllib.parse import urljoin

from museums.items import ObjectItem

class MuseumseuSpider(scrapy.Spider):
    name = 'museumseu'
    allowed_domains = ['museums.eu']
    start_urls = ['http://museums.eu/search/index?documenttype=collection&page=1']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_collection_list)

    def parse_collection_list(self, response):
        for l in response.xpath('//h4[@class="media-heading"]/a/@href').getall():
            yield response.follow(l, callback=self.parse_object_list)

        for l in response.xpath('//ul[@class="pagination"]/li/a/@href'):
            yield response.follow(l, callback=self.parse_collection_list)

    def parse_object_list(self, response):
        for l in response.xpath('//div[@class="artwork"]/a/@href').getall():
            yield response.follow(l, callback=self.parse_object_page)

        for l in response.xpath('//ul[@id="collection-pagination"]/li/a/@href').getall():
            yield response.follow(l, callback=self.parse_object_list)

    def parse_object_page(self, response):
        item = ObjectItem()

        item['object_number'] = response.xpath('//dt[text()="Inventory Number"]/following-sibling::dd/text()').get()
        item['institution_name'] = response.xpath('//ol[@class="breadcrumb"]//a[starts-with(@href, "/museum/details/")]/text()').get()
        item['department'] = response.xpath('//dt[text()="Collection"]/following-sibling::dd/a/text()').get()
        item['category'] = response.xpath('//dt[text()="Object Type"]/following-sibling::dd/text()').get()
        item['title'] = response.xpath('//h1/text()').get()
        item['description'] = response.xpath('//hr[@class="sem-separator"]/preceding-sibling::p/text()').get()
        item['dimensions'] = response.xpath('//dt[text()="Measurements"]/following-sibling::dd/text()').get()
        item['materials'] = response.xpath('//dt[text()="Materials"]/following-sibling::dd/text()').get()
        item['technique'] = response.xpath('//dt[text()="Techniques"]/following-sibling::dd/text()').get()
        item['date_description'] = response.xpath('//dt[text()="Time of Origin"]/following-sibling::dd/text()').get()
        item['maker_full_name'] = response.xpath('//dt[text()="Author"]/following-sibling::dd/text()').get()
        item['image_url'] = response.xpath('//a[@id="mainPicture"]/img/@src').get()
        if item['image_url'] is not None:
            item['image_url'] = urljoin(response.url, item['image_url'])

        item['source_1'] = response.url

        yield item

