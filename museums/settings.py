# Scrapy settings for museums project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "museums"

SPIDER_MODULES = ["museums.spiders"]
NEWSPIDER_MODULE = "museums.spiders"

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 32
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'museums.middlewares.MuseumsSpiderMiddleware': 543,
# }

BRIGHT_DATA_ENABLED = False
BRIGHT_DATA_ZONE_USERNAME = "lum-customer-c_cecd546c-zone-zone_unlocker_bostonmfa"
BRIGHT_DATA_ZONE_PASSWORD = "lhob01y5af37"

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    #'museums.middlewares.BrightDataDownloaderMiddleware': 500,
    'aroay_cloudscraper.downloadermiddlewares.CloudScraperMiddleware': 543, # pip3 install aroay-cloudscraper
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

TWILIO_ACCOUNT_SID = "AC66f9624c713fb8403dc4a153c3f69615"
TWILIO_API_TOKEN = "de07859809be34d8237013db5381a7d2"
FROM_PHONE_NUMBER = "+19807372044"
TO_PHONE_NUMBER = "+37061021232"
GOOGLE_API_KEY = "AIzaSyDc_6DfkpFdeQJX-KK7t_2k26aOdi-4aqU"

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "museums.pipelines.ConstraintEnforcementPipeline": 250,
    "museums.pipelines.InstitutionGeoEnrichmentPipeline": 275,
    #'museums.pipelines.NotificationPipeline': 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.DbmCacheStorage"
HTTPCACHE_GZIP = True
HTTPCACHE_ALWAYS_STORE = True
HTTPCACHE_IGNORE_HTTP_CODES = [503, 504, 505, 502, 500, 400, 401, 402, 403, 404, 429]

RETRY_TIMES = 8
