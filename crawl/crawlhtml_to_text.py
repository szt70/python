#!/usr/bin/env python
# coding:utf-8
'''
    クロールデータからテキストのみ抽出して出力
'''

import sys
import os
import traceback
import json
import urllib
import yaml
from common.net.scraping import Scraping
from common.net.perser import htmlPerser
from datetime import datetime
from bs4 import BeautifulSoup 
import hashlib
from lib2to3.pgen2 import driver
from selenium import webdriver
from urllib.parse import urljoin
import MeCab
import config
from common.lang import stringUtils
from common.file import fileUtils
from common.log import logging
logger = logging.getLogger("test")


def toText() :
    '''
        クロールデータのHTMLファイルをテキストファイルのみに整形して出力します
    '''
    dir = config.get("crawl", "crawldata.dir.path")
    textDir = config.get("crawl", "text.dir.path")
    fileUtils.makedirs(textDir)

    list = os.listdir(dir)
    for file in list:
        filePath = dir + file
        if os.path.isfile(filePath) :
            f = open(filePath,'r', encoding='utf-8-sig')
            try :
                crawlData = json.load(f)
            except:
                logger.exception("Could not load %s" % filePath + " ", traceback.format_exc())
                continue
            f.close()
            text = crawlData["html"]
            outputFile = textDir + os.path.splitext(file)[0] + ".txt"
           
            f = open(outputFile, 'w', encoding='utf-8-sig')
            f.write(text)
            f.close()


if __name__ == "__main__":
    logger.debug("Start html to text")

    toText()

    logger.debug("End html to text")