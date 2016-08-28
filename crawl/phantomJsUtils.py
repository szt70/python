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
logger = config.getLogger("test")

class PhantomJsUtils(object):

    __instance = None
    __phantomJsDriver = None

    def __new__(cls, *args, **keys):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            log_name = "/tmp/phantomjs.log" #ログを出力しない場合はos.path.devnull
            userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"
            
            timeDriverStart = time.clock()
            cls.__phantomJsDriver = webdriver.PhantomJS(
                desired_capabilities={
                    'phantomjs.page.settings.userAgent': userAgent,
                },
                service_log_path=log_name
                                     )
            timeDriverEnd = round(time.clock() - timeDriverStart, 3)
            logger.debug("PhantomJs Driver init : {0}s".format(timeDriverEnd))
        
        return cls.__instance


    def getPhantomJsDriver(self):
        return self.__phantomJsDriver
