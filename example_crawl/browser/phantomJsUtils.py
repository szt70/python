#!/usr/bin/env python
# coding: utf-8
"""
スクレイピング
"""
__author__ = "szt70"
__version__ = "0.0.1"
__date__    = "2016-08-18"

import logging
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re

class PhantomJsUtils(object):

    __instance = None
    __phantomJsDriver = None

    def __new__(cls, *args, **keys):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            log_name = "/tmp/phantomjs.log" #ログを出力しない場合はos.path.devnull
            userAgent = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"
            
            timeDriverStart = time.clock()
            cls.__phantomJsDriver = webdriver.PhantomJS(
                desired_capabilities={
                    'phantomjs.page.settings.userAgent': userAgent,
                },
                service_log_path=log_name
                                     )
            timeDriverEnd = round(time.clock() - timeDriverStart, 3)
            logging.debug("PhantomJs Driver init : {0}s".format(timeDriverEnd))
        
        return cls.__instance


    def getPhantomJsDriver(self):
        return self.__phantomJsDriver


if __name__ == '__main__':

    print ("test start")
    url = "http://headlines.yahoo.co.jp/hl?a=20161031-00000118-spnannex-ent"
    timeStart = time.clock();
    
    pjs = PhantomJsUtils()
    driver = pjs.getPhantomJsDriver()
    
    timeGetStart = time.clock()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    print("soup : {0}".format(soup))
    timeGetEnd = round(time.clock() - timeGetStart, 3)

    article_text = soup.find(class_=re.compile('ynDetailText'))
    print("text : {0}".format(article_text))
    timeTotal = round(time.clock() - timeStart, 3)
    print("scraping(phantomJs) {0} {1}s(get:{2}s)".format( url, timeTotal, timeGetEnd))
