import scrapy

from urllib.parse import urljoin

from museums.items import ObjectItem

class VictoriaSpider(scrapy.Spider):
    name = 'victoria'
    allowed_domains = ['collections.museumsvictoria.com.au']
    start_urls = ['https://collections.museumsvictoria.com.au/search?query=&page=1&perpage=100']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_page)

    def parse_search_page(self, response):
        object_links = response.xpath('//div[@id="maincontent"]/div/a/@href').getall()
        for object_link in object_links:
            url = urljoin(response.url, object_link)
            yield scrapy.Request(url, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[@title="Next page"]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_search_page)

    def parse_object_page(self, response):
        item = ObjectItem()

        item['object_number'] = response.xpath('//input[@name="documentId"]/@value').get()
        item['institution_name'] = 'Museums Victoria'
        item['institution_city'] = 'Melbourne'
        item['institution_state'] = 'Victoria'
        item['institution_country'] = 'Australia'
        # XXX: institution_latitude, institution_longitude
        item['department'] = response.xpath('//li[./h3[text()="Discipline"]]/p/a/text()').get()
        item['category'] = response.xpath('//li[./h3[text()="Category"]]/p/a/text()').get()
        item['title'] = " ".join(response.xpath('//h1[@id="maincontent"]/text()').getall()).strip()
        item['description'] = "\n".join(response.xpath('//div[@class="summary"]/*/text()').getall())
        # XXX: current_location
        item['dimensions'] = response.xpath('//li[./h3[contains(text(),"Overall Dimensions")]]/p/text()').get("").strip()
        item['inscription'] = response.xpath('//li[./h3[text()="Inscriptions"]]/p/text()').get()
        # XXX: provenance, materials, technique, from_location, culture, date_description
        # year_start, year_end
        item['maker_full_name'] = response.xpath('//li[./h3[text()="Artist" or text()="Author"]]/p/a[1]/text()').get()
        
        maker_years = response.xpath('//li[./h3[text()="Artist" or text()="Author"]]/p/a[contains(@href, "date")]/text()').get()
        if maker_years is not None and "-" in maker_years:
            item['maker_birth_year'] = maker_years.split("-")[0]
            item['maker_death_year'] = maker_years.split("-")[-1]

        item['acquired_from'] = response.xpath('//li[./h3[text()="Acquisition Information"]]/p/text()').get()
        item['image_url'] = response.xpath('//div[@class="hero-media"]/img/@src').get()
        if item.get('image_url') is not None:
            item['image_url'] = urljoin(response.url, item['image_url'])

        item['source_1'] = response.url

        yield item

