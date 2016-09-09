#!/usr/bin/env python
# coding: utf-8
"""
HTMLパーサー
"""
__author__ = "szt70"
__version__ = "0.0.1"
__date__    = "2016-08-18"

import yaml
import re
import sys
import json
import os
import time
import math
from lib2to3.pgen2 import driver

import requests
import re
from bs4 import BeautifulSoup,NavigableString, Declaration, Comment
from selenium import webdriver
import config
from common.lang import stringUtils
from common.log import logging
logger = logging.getLogger("test")

class HTMLParser():

    def get(self, url, source):
        '''
            HTMLタグを除去したテキストを取得
            
        '''
        
        soup = BeautifulSoup(source, "lxml")
        text = self.__getNavigableStrings(soup)
        text = stringUtils.collect_line_break(text)
        return text

    def __getNavigableStrings(self, soup):
        script = soup("script")
        for tag in script:
            tag.extract()
        style = soup("style")
        for tag in style:
            tag.extract()

        body = soup.body
        text = body.getText()
        text = self.strip_tags(text)
        return text

    def strip_tags(self, html):
        '''
            HTMLタグを除去する
            閉じられてない等不正タグは除去されない
        '''
        p = re.compile(r"<[^>]*?>")
        return p.sub("", html)
