import scrapy

from urllib.parse import urljoin

from museums.items import ObjectItem

class PennSpider(scrapy.Spider):
    name = 'penn'
    allowed_domains = ['www.penn.museum']
    start_urls = ['https://www.penn.museum/collections/search.php?term=&submit_term=Submit+Query&type%5B%5D=1']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search_results)

    def parse_search_results(self, response):
        for object_link in response.xpath('//a[./img[contains(@class, "center-block")]]/@href').getall():
            object_url = urljoin(response.url, object_link) 
            yield scrapy.Request(object_url, callback=self.parse_object_page)

        next_page_link = response.xpath('//a[text()="Next"]/@href').get()
        if next_page_link != "#":
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_search_results)

    def parse_object_page(self, response):
        item = ObjectItem()
        
        item['object_number'] = response.xpath('//span[@itemprop="identifier"]/text()').get()
        item['institution_name'] = 'Penn Museum'
        item['institution_city'] = 'Philadelphia'
        item['institution_state'] = 'PA'
        item['institution_country'] = 'USA'
        item['institution_latitude'] = 39.952305
        item['institution_longitude'] = -75.193703
        item['department'] = response.xpath('//tr[./th[text()="Section:"]]/td/text()').get()
        item['title'] = response.xpath('//h1[@itemprop="name"]/text()').get("").strip()
        item['description'] = " ".join(response.xpath('//div[@itemprop="description"]/*/text()').getall())
        item['current_location'] = response.xpath('//tr[./th[contains(text(),"Current Location:")]]/td/text()').get("").strip()
        if item['current_location'] == '':
            item['current_location'] = response.xpath('//tr[./th[contains(text(),"Current Location:")]]/td/a/text()').get("").strip()
        item['dimensions'] = ""

        height = response.xpath('//tr[./th[text()="Height:"]]/td/text()').get()
        if height is not None:
            item['dimensions'] += "Height: " + height + " "
        width = response.xpath('//tr[./th[text()="Width:"]]/td/text()').get()
        if width is not None:
            item['dimensions'] += "Width: " + width + " "
        length = response.xpath('//tr[./th[text()="Length:"]]/td/text()').get()
        if length is not None:
            item['dimensions'] += "Length: " + length + " "
        thickness = response.xpath('//tr[./th[text()="Thickness: "]]/td/text()').get()
        if thickness is not None:
           item['dimensions'] += "Thickness: " + thickness + " "
        outside_diameter = response.xpath('//tr[./th[text()="Outside Diameter:"]]/td/text()').get()
        if outside_diameter is not None:
            item['dimensions'] += "Outside Diameter: " + outside_diameter + " "
        item['provenance'] = " ".join(response.xpath('//tr[./th[text()="Provenience: "]]/td/text()').getall())
        item['materials'] = " ".join(response.xpath('//tr[./th[text()="Materials:"]]/td/text()').getall())
        item['technique'] = response.xpath('//tr[./th[text()="Technique:"]]/td/text()').get()
        item['from_location'] = response.xpath('//tr[./th[text()="Locus: "]]/td/text()').get()
        item['culture'] = response.xpath('//tr[./th[text()="Culture Area: "]]/td/text()').get()
        item['date_description'] = response.xpath('//tr[./th[text()="Date Made: "]]/td/text()').get()
        item['year_start'] = response.xpath('//tr[./th[text()="Early Date: "]]/td/text()').get()
        item['year_end'] = response.xpath('//tr[./th[text()="Late Date: "]]/td/text()').get()
        item['maker_full_name'] = response.xpath('//tr[./th[text()="Maker: "]]/td/text()').get()
        item['credit_line'] = response.xpath('//tr[./th[text()="Credit Line:"]]/td/a/text()').get()
        item['image_url'] = response.xpath('//img[@itemprop="image"]/@src').get()
        item['source_1'] = response.url

        yield item

