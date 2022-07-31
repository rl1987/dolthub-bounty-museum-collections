import scrapy


class BristolSpider(scrapy.Spider):
    name = 'bristol'
    allowed_domains = ['museums.bristol.gov.uk']
    start_urls = ['https://museums.bristol.gov.uk/list.php']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_object_list)

    def parse_object_list(self, response):
        for l in response.xpath('//div[@class="media"]//a/@href').getall():
            yield response.follow(l, callback=self.parse_object_page)

        next_page_link = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page_link is not None:
            yield response.follow(next_page_link, callback=self.parse_object_list)

    def parse_object_page(self, response):
        pass
