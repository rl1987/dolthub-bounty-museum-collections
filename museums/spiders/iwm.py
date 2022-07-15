import scrapy

from urllib.parse import urljoin

from museums.items import ObjectItem

class IwmSpider(scrapy.Spider):
    name = 'iwm'
    allowed_domains = ['iwm.org.uk']
    start_urls = ['https://www.iwm.org.uk/collections/search?query=&pageSize=30&media-records=all-records&page=1']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        links = response.xpath('//div[@class="teaser-list__title--content"]/a/@href').getall()
        for l in links:
            url = urljoin(response.url, l)
            yield scrapy.Request(url, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[@title="Go to next page"]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        item = ObjectItem()
        
        item['object_number'] = response.xpath('//dt[text()="Catalogue number"]/following-sibling::dd/text()').get()
        item['institution_name'] = 'Imperial War Museum'
        item['institution_city'] = 'London'
        item['institution_state'] = 'England'
        item['institution_country'] = 'United Kingdom'
        item['institution_latitude'] = 51.4981985
        item['institution_longitude'] = -0.1196327
        item['category'] = response.xpath('//dt[text()="Category"]/following-sibling::dd/a/text()').get()
        item['title'] = response.xpath('//h1[@class="hero__truncate"]/text()').get("").strip()
        item['description'] = response.xpath('//div[@class="object-description__text"]/text()').get()
        item['dimensions'] = "|".join(response.xpath('//dt[text()="Dimensions"]/following-sibling::dd/p/text()').getall())
        item['materials'] = "|".join(response.xpath('//dt[text()="Materials"]/following-sibling::dd/p/text()').getall())
        item['from_location'] = response.xpath('//dt[text()="Place made"]/following-sibling::dd/a/text()').get()
        item['date_description'] = response.xpath('//dt[text()="Production date"]/following-sibling::dd/text()').get()
        item['maker_full_name'] = "|".join(response.xpath('//dt[text()="Creator"]/following-sibling::dd/a/text()').getall())
        item['image_url'] = response.xpath('//meta[@property="og:image"]/@content').get()
        item['source_1'] = response.url

        yield item
