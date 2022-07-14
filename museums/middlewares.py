# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import scrapy
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

import logging
import time

class MuseumsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# Based on:
# https://stackoverflow.com/questions/43630434/how-to-handle-a-429-too-many-requests-response-in-scrapy
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from scrapy.http import FormRequest

import time
from urllib.parse import urlparse, parse_qsl

class RateLimitDownloaderMiddleware(RetryMiddleware):
    def __init__(self, crawler):
        super(RateLimitDownloaderMiddleware, self).__init__(crawler.settings)
        self.crawler = crawler
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        elif response.status == 429:
            o = urlparse(response.url)
            if o.netloc == 'www.google.com':
                params = dict(parse_qsl(o.query))
                request = scrapy.Request(params['continue'], callback=request.callback)

            #self.crawler.engine.pause()
            time.sleep(5)
            #self.crawler.engine.unpause()
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        elif response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response 

from museums.settings import BRIGHT_DATA_ENABLED, BRIGHT_DATA_ZONE_USERNAME, BRIGHT_DATA_ZONE_PASSWORD

from w3lib.http import basic_auth_header

import random

class BrightDataDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        if not BRIGHT_DATA_ENABLED:
            return

        request.meta['proxy'] = 'http://zproxy.lum-superproxy.io:22225'
        
        username = BRIGHT_DATA_ZONE_USERNAME + "-session-" + str(random.random())

        request.headers['Proxy-Authorization'] = basic_auth_header(username, BRIGHT_DATA_ZONE_PASSWORD)

