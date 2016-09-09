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
import config
from common.browser.phantomJsUtils import PhantomJsUtils
from common.log import logging
logger = logging.getLogger("test")

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
        
        pjs = PhantomJsUtils()
        driver = pjs.getPhantomJsDriver()
        #JSON形式のファイルからCookie読み込み
        f = open("c:/tmp/cookie.json")
        cookieList = json.load(f)

        for c in cookieList:
            driver.add_cookie(c)
        timeGetStart = time.clock()
        driver.get(url)
        html = driver.page_source
        timeGetEnd = round(time.clock() - timeGetStart, 3)

        timeTotal = round(time.clock() - timeStart, 3)
        logger.debug("scraping(phantomJs) {0} {1}s(get:{2}s)".format( url, timeTotal, timeGetEnd))
        return html
