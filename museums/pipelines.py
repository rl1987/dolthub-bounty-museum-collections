# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from museums.settings import TWILIO_ACCOUNT_SID, TWILIO_API_TOKEN, FROM_PHONE_NUMBER, TO_PHONE_NUMBER

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from twilio.rest import Client

class NotificationPipeline:
    def close_spider(self, spider):
        msg = "Spider {} finished scraping.".format(spider.name)

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_API_TOKEN)
        message = client.messages.create(body=msg, from_=FROM_PHONE_NUMBER, to=TO_PHONE_NUMBER)

        spider.logger.info(message)
