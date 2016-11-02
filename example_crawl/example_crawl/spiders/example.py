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

'''

    1) HOMEディレクトリ以下の全PythonでExampleを任意の文字列に変更
　  
    2) settings.pyを編集
    　　　　　scrapyログ ... LOG_FILE
                結果出力先 ... FEED_URI
　　　　　　その他設定
    
    3) parse_itemでパース処理
        Ajaxページの場合はscraping_phantomJsを呼び出す

    3) 実行
       $ cd HOME_DIRECTORY
       $ scrapy crawl <name>
'''
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
            # スクレイピングしないがspiderがたどるURLを指定、follow=Trueで再帰的に
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
        #soup = self.scraping_phantomJs(url)#ynDetailText
        #article_text_tag = soup.find(class_=re.compile('ynDetailText'))
        #article_text = article_text_tag.text
        article_text = response.xpath('//p[@class="ynDetailText"]/text()').extract()
        if article_text is None or len(article_text) == 0:
            logging.debug("none hit tag : {0}".format(url))
            return
        #logging.debug("article_text : {0}".format(article_text))
        article = ExampleCrawlItem()
        article['url'] = url
        article['title'] = response.selector.xpath('//title/text()').extract()[0].replace('\n','')
        article['text'] = ' '.join(article_text).replace('\n','')
        article['datetime'] = self.datetime_str();
        logging.debug("get ParseText : {0}".format(url))
        #スクレイピング結果を出力
        yield article 
            
        #ページ内の全てのaタグリンクをクロール
        linklist = response.xpath('//a/@href').extract()
        for link in linklist:
            # 次のクロール対象を渡す
            yield scrapy.Request(response.urljoin(link), callback=self.parse)


    def scraping_phantomJs(self, url):
        """ 
            Ajaxページのスクレイピング
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


