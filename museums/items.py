# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# https://www.dolthub.com/repositories/dolthub/museum-collections/doc/main
class ObjectItem(scrapy.Item):
    object_number = scrapy.Field()
    institution_name = scrapy.Field()
    institution_city = scrapy.Field()
    institution_state = scrapy.Field()
    institution_country = scrapy.Field()
    institution_latitude = scrapy.Field()
    institution_longitude = scrapy.Field()
    department = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    current_location = scrapy.Field()
    dimensions = scrapy.Field()
    inscription = scrapy.Field()
    provenance = scrapy.Field()
    materials = scrapy.Field()
    technique = scrapy.Field()
    from_location = scrapy.Field()
    culture = scrapy.Field()
    date_description = scrapy.Field()
    year_start = scrapy.Field()
    year_end = scrapy.Field()
    maker_full_name = scrapy.Field()
    maker_first_name = scrapy.Field()
    maker_last_name = scrapy.Field()
    maker_birth_year = scrapy.Field()
    maker_death_year = scrapy.Field()
    maker_role = scrapy.Field()
    maker_gender = scrapy.Field()
    acquired_year = scrapy.Field()
    acquired_from = scrapy.Field()
    accession_year = scrapy.Field()
    accession_number = scrapy.Field()
    credit_line = scrapy.Field()
    image_url = scrapy.Field()
    source_1 = scrapy.Field()
    source_2 = scrapy.Field()
