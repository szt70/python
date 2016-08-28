#!/usr/bin/env python
# coding: utf-8
"""
スクレイピング
"""
__author__ = "szt70"
__version__ = "0.0.1"
__date__    = "2016-08-18"

import yaml
import sys
import json
import os
import time
import math
from lib2to3.pgen2 import driver

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from logging import config,getLogger
config.dictConfig(yaml.load(open("logging.conf", encoding='UTF-8').read()))
logger = getLogger("test")

class Scraping:


    def scraping_requests(self, url):
        """ requests利用してスクレイピング
        """
        timeStart = time.clock();
        # get a HTML response
        response = requests.get(url)
        html = response.text.encode(response.encoding)  # prevent encoding errors
        # parse the response
        timeTotal = round(time.clock() - timeStart, 3);
        logger.debug("scraping {0} {1}s".format( url, timeTotal))
        return html

    def scraping(self, url):
        """ ユーザーエージェント、Cookieを設定してスクレイピング
        """
        timeStart = time.clock();
        log_name = "/tmp/phantomjs.log" #ログを出力しない場合はos.path.devnull
        userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"
        driver = webdriver.PhantomJS(
            desired_capabilities={
                'phantomjs.page.settings.userAgent': userAgent,
            },
            service_log_path=log_name
                                     )
        #JSON形式のファイルからCookie読み込み
        f = open("c:/tmp/cookie.json")
        cookieList = json.load(f)

        for c in cookieList:
            driver.add_cookie(c)
        driver.get(url)
        html = driver.page_source

        timeTotal = round(time.clock() - timeStart, 3);
        logger.debug("scraping(phantomJs) {0} {1}s".format( url, timeTotal))
        return html
