import scrapy

from urllib.parse import urljoin

class HermitageSpider(scrapy.Spider):
    name = 'hermitage'
    allowed_domains = ['hermitagemuseum.org']
    start_urls = ['https://www.hermitagemuseum.org/wps/portal/hermitage/explore/artworks/!ut/p/z1/jY7BCoJAEIafxSeYHTV1j8PGrikySpruXsJLIaV1iJ4_iQ4VJP23H76Z7wcHHbipvw_H_jZcpv48d-uiPRNFGCiRsSmloBwx4lQXuomhfQLiR0iA--d-AXDL71twnwqjzVqQkZVKQvZNgt8Ab_JYENerlHmnfBW-gAWJnUfGb4pKzSMVNZihTlEGsAVbgK3qQyAJrmPTiaEcT-R5D0bsitM!/p0/IZ7_OAA613C0JGQC90ACAU1J1FH193=CZ6_OAA613C0JOGP90AK116OHFMFU7=MKQFBTf39A=GK=/#Z7_OAA613C0JGQC90ACAU1J1FH193']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_list_of_categories)

    def parse_list_of_categories(self, response):
        #for category_link in response.xpath('//div[@class="her-col-100"]/a/@href').getall():
        #    category_url = response.url.split("?")[0] + category_link
        #    yield scrapy.Request(category_url, callback=self.parse_list_of_artworks)
            
        next_page_link = response.xpath('//a[@title="Link to next page"]/@href').get()
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link)
            yield scrapy.Request(next_page_url, callback=self.parse_list_of_categories)

    def parse_list_of_artworks(self, response):
        pass

    def parse_artwork_page(self, response):
        pass
