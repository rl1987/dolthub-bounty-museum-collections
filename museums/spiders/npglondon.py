import scrapy

import string

from museums.items import ObjectItem

class NpglondonSpider(scrapy.Spider):
    name = 'npglondon'
    allowed_domains = ['www.npg.org.uk']
    start_urls = [ "https://www.npg.org.uk/collections/search/arta-z/?index=" + letter for letter in string.ascii_lowercase ] + [ 'https://www.npg.org.uk/collections/search/sita-z/?index=' + letter for letter in string.ascii_lowercase ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_artist_list)

    def parse_artist_list(self, response):
        for l in response.xpath('//div[@id="eventsListing"]/p/a/@href').getall():
            yield response.follow(l, callback=self.parse_portrait_list)

    def parse_portrait_list(self, response):
        for l in response.xpath('//p[@class="eventHeading"]/a/@href').getall():
            yield response.follow(l, callback=self.parse_portrait_page)

    def parse_portrait_page(self, response):
        item = ObjectItem()

        item['object_number'] = response.xpath('//title/text()').get().split(";")[0]
        item['institution_name'] = "National Portrait Gallery"
        item['institution_city'] = "London"
        item['institution_state'] = 'England'
        item['institution_country'] = "United Kingdom"
        item['institution_latitude'] = 51.5094236
        item['institution_longitude'] = -0.1303103
        item['title'] = response.xpath('//title/text()').get().split("; ")[-1].replace(" - National Portrait Gallery", "")
        item['description'] = response.xpath('//meta[@property="og:description"]/@content').get()
        item['maker_full_name'] = "|".join(response.xpath('//ul[@id="artist-list"]//a/text()').getall())
        maker_roles = response.xpath('//ul[@id="artist-list"]/li/text()').getall()
        maker_roles = list(map(lambda mr: mr.split(", ")[-1].split(". ")[0], maker_roles))
        maker_roles = "|".join(maker_roles)
        item['maker_role'] = maker_roles

        lines = response.xpath('//div[@class="contentColumn last"]/p[last()]/text()').getall()
        item['technique'] = ", ".join(lines[1].split(", ")[:-1])
        item['date_description'] = lines[1].split(", ")[-1]
        item['dimensions'] = lines[2]

        try:
            item['acquired_year'] = int(lines[3].split(", ")[-1])
            item['acquired_from'] = lines[3].split(", ")[0]
        except:
            pass

        item['image_url'] = response.xpath('//img[@class="zoom-fallback"]/@src').get()
        item['source_1'] = response.url

        yield item

