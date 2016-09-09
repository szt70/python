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
from bs4 import BeautifulSoup,NavigableString, Declaration, Comment
from selenium import webdriver
import config
logger = config.getLogger("test")

class HTMLParser():

    def get(self, url, source):
        
        soup = BeautifulSoup(source, "lxml")
        text = self.__getNavigableStrings(soup)
        text = re.sub(r'\n+', '\n', text)
        return text

    def __getNavigableStrings(self, soup):
        body = soup.find("body").text
        return body
