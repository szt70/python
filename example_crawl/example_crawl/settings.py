# -*- coding: utf-8 -*-

# Scrapy settings for example_crawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

#　シードURLのファイル形式
FEED_FORMAT = 'jsonlines'

# シードURLの保存先
FEED_URI = 'file:///tmp/export.json'

BOT_NAME = 'example_crawl'

SPIDER_MODULES = ['example_crawl.spiders']
NEWSPIDER_MODULE = 'example_crawl.spiders'

#拡張した Exporter を登録
FEED_EXPORTERS = {          
    'jsonlines': 'example_crawl.exporters.NonEscapeJsonLinesItemExporter',  
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#ユーザーエージェント
USER_AGENT = 'example_crawl (+http://www.yourdomain.com)'

# Obey robots.txt rules
#True = Webサイトのrobots.txtに従う
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

#Webページのダウンロード間隔
DOWNLOAD_DELAY = 1

#ログ出力先
LOG_FILE = '/tmp/scrapy.log'

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'example_crawl.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'example_crawl.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'example_crawl.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

##########################################################################
#
# 独自設定
#
##########################################################################

# スクレイピング許可ドメイン、複数指定可
ALLOWED_DOMAINS = ["news.yahoo.co.jp", "headlines.yahoo.co.jp"]

# スクレイピングを開始するURL、複数指定可
START_URLS = ['http://news.yahoo.co.jp/']

#Cookie
COOKIES = {
    "test":"value"
}

# PhantomJs用
COOKIES_LIST=[
    {
        "domain": ".test.com",
        "name": "__gads",
        "path": "/",
        "value": "ID=641422a78e56efd3:T=1414935735:S=ALNI_MYaaiv5JGTIabD0RybbFbROSYGYgg"
    },
    ]