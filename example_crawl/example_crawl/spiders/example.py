# -*- coding: utf-8 -*-
import logging
import scrapy
import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.conf import settings
from example_crawl.items import ExampleCrawlItem
from datetime import datetime
import time
from browser.phantomJsUtils import PhantomJsUtils
from bs4 import BeautifulSoup

class ExampleSpider(CrawlSpider):
    name = "example"
    
    #スクレイピング許可ドメイン、複数指定可
    allowed_domains = settings.get("ALLOWED_DOMAINS")
    
    # スクレイピングを開始するURL、複数指定可
    start_urls = settings.get("START_URLS")
    
    # スクレイピング対象のパスパターン、ドメイン以下のURLに関して正規表現で指定します
    allow_list = ['/hl']
    
    # スクレイピング対象外パスパターン、ドメイン以下のURLに関して正規表現で指定します
    deny_list = ['view-000']

    rules = (
            # スクレイピングするURLのルールを指定
            Rule(LinkExtractor( allow=allow_list, deny=deny_list), callback='parse_item'),
            # spiderがたどるURLを指定
            Rule(LinkExtractor(), follow=True),
        )

    def make_requests_from_url(self, url):
        '''
        Resuest実行前に呼ばれるメソッド
        '''
        cookies = settings.get("COOKIES")
        #Cookieを設定
        request = super(ExampleSpider, self).make_requests_from_url(url)
        for k, v in cookies.items():
            request.cookies[k] = v
        return request
    
    def datetime_str(self):
        tdatetime = datetime.now()
        tstr = tdatetime.strftime('%Y/%m/%d %H:%M:%S')
        return tstr
    
    def parse_item(self, response):
        '''
        Parse処理メソッド、Spiderクラス内で定義しているRuleクラスのコールバック関数で指定している
        '''
        url = response.urljoin('')
        logging.debug("crawl_url item : {0}".format(url))
        soup = self.scraping_phantomJs(url)
        article_text = soup.select('p.ynDetailText')
        logging.debug("article_text : {0}".format(article_text))
        #article_text = response.xpath('//p[@class="ynDetailText"]/text()').extract()
        article = ExampleCrawlItem()
        article['url'] = url
        article['title'] = response.selector.xpath('//title/text()').extract()[0].replace('\n','')
        article['text'] = ' '.join(article_text).replace('\n','')
        article['datetime'] = self.datetime_str();
        #スクレイピング結果を出力
        yield article 
            
        #ページ内の全てのaタグリンクをクロール
        linklist = response.xpath('//a/@href').extract()
        for link in linklist:
            # 次のクロール対象を渡す
            yield scrapy.Request(response.urljoin(link), callback=self.parse)


    def scraping_phantomJs(self, url):
        """ ユーザーエージェント、Cookieを設定してスクレイピング
        """
        timeStart = time.clock();
        
        pjs = PhantomJsUtils()
        driver = pjs.getPhantomJsDriver()
        
        #JSON形式のcookie読み込み
        cookies = settings.get("COOKIES_LIST")

        for c in cookies:
            driver.add_cookie(c)
        timeGetStart = time.clock()
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        timeGetEnd = round(time.clock() - timeGetStart, 3)

        timeTotal = round(time.clock() - timeStart, 3)
        logging.debug("scraping(phantomJs) {0} {1}s(get:{2}s)".format( url, timeTotal, timeGetEnd))
        return soup


