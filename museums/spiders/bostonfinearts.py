import scrapy

from museums.items import ObjectItem

class BostonFineArtsSpider(scrapy.Spider):
    name = 'bostonfinearts'
    allowed_domains = ['collections.mfa.org']
    start_urls = ['https://collections.mfa.org/search/objects/*/*']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        links = response.xpath('//div[@class="grid-item-inner"]//h3/a/@href').getall()
        for l in links:
            yield response.follow(l, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[contains(@class, "next-page-link")]/@href').get()
        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse_search_page)

    def parse_object_page(self, response):
        item = ObjectItem()
    
        item['institution_name'] = 'Museum of Fine Arts Bostom'
        item['institution_city'] = 'Boston'
        item['institution_state'] = 'MA'
        item['institution_country'] = 'United States of America'
        item['institution_latitude'] = 42.339381
        item['institution_longitude'] = -71.0962367
        item['department'] = response.xpath('//div[contains(@class, "collectionTermsField")]/span[@class="detailFieldValue"]/a/text()').get()
        item['category'] = response.xpath('//div[contains(@class, "classificationsField")]/span[@class="detailFieldValue"]/a/text()').get()
        item['title'] = response.xpath('//div[contains(@class, "titleField")]/h2/text()').get()
        item['description'] = " ".join(response.xpath('//div[contains(@class, "descriptionField")]/span[@class="detailFieldValue"]/text()').getall())
        if item['description'] == '':
            item['description'] = " ".join(response.xpath('//div[contains(@class, "webDescriptionField")]/text()').getall()).strip()

        item['current_location'] = response.xpath('//div[contains(@class, "onviewField")]/a/text()').get("").strip()
        item['dimensions'] = response.xpath('//div[contains(@class, "dimensionsField")]/span[@class="detailFieldValue"]/text()').get("").strip()
        item['inscription'] = " ".join(response.xpath('//div[contains(@class, "inscribedField")]/span[@class="detailFieldValue"]/text()').getall())
        item['provenance'] = response.xpath('//div[contains(@class, "provenanceField")]/span[@class="detailFieldValue"]/text()').get("").strip()
        item['materials'] = response.xpath('//div[contains(@class, "mediumField")]/span[@class="detailFieldValue"]/text()').get("").strip()
        item['from_location'] = response.xpath('//div[contains(@class, "objectGeographyField")]/text()').get()
        item['culture'] = response.xpath('//div[contains(@class, "cultureField")]/text()').get("").strip()
        item['date_description'] = response.xpath('//div[contains(@class, "displayDateField")]/text()').get("").strip()
        item['maker_full_name'] = "|".join(response.xpath('//div[contains(@class, "peopleField")]/a/text()').getall())
        item['accession_number'] = response.xpath('//div[contains(@class, "invnolineField")]/span[@class="detailFieldValue"]/text()').get()
        item['credit_line'] = response.xpath('//div[contains(@class, "creditlineField")]/span[@class="detailFieldValue"]/text()').get("").strip()
        item['image_url'] = response.xpath('//meta[@name="og:image"]/@content').get()
        item['source_1'] = response.url.split(";")[0]

        try:
            item['object_number'] = response.url.split('/')[4]
        except:
            item['object_number'] = item['accession_number']

        yield item
