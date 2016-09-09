#!/usr/bin/env python
# coding:utf-8
'''
    分かち書きを行う
'''

import sys
import re
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
from common.log import logging
logger = logging.getLogger("test")


def wakati(text) :
    '''
        半角スペースで分かち書きした文字列を取得する
    '''

    tagger = MeCab.Tagger("-O wakati")
    wakati_text = []
    #STOP_WORD = " 。 、 「 」 （ ） ? ？ ： ， , ． ! ！ # $ % & ' ( ) = ~ | ` { } * + ? _ > [ ] @ : ; / . ¥ ^ 【 】 ￥ ＿ ／ 『 』 ＞ ？ ＿ ＊ ＋ ｀ ｜ 〜 ＊ ＋ ＞ ？ ＃ ” ＃ ＄ ％ ＆ ’ \" ・".split()
    
    wakati_formalize = []
    text = re.sub(r'\r\n', '\n', text)
    text = stringUtils.collect_line_break(text)
    for row in text.split('\n'):
        row = text_format(row)
        if not row :
            continue 
        wakati_raw = tagger.parse(row) 
        wakati_raw = wakati_raw.strip()
        wakati_formalize.append(wakati_raw)
    wakati_text.append(' '.join(wakati_formalize))
    return ' '.join(wakati_text)

def text_format(text) :
    '''
    解析前の文字列フォーマット
    '''
    format = stringUtils.collect_line_break(text)
    format = re.sub(r'\r\n', '\n', format)
    format = stringUtils.removeHalfSymbol(format)
    format = stringUtils.removeControlCharacter(format)
    return format

def text_to_wakati() :
    '''
       フォーマット済みのテキストファイルを読み込んで分かち書きでファイル出力
    '''

    textDir = config.get("crawl", "text.dir.path")
    if not os.path.isdir(textDir):
        logger.debug("not found text dir {0}".format(textDir));
        return
 
    wakati_text = []
    list = os.listdir(textDir)
    for file in list:
        filePath = textDir + file
        if os.path.isfile(filePath) :
            f = open(filePath,'r', encoding='utf-8-sig')
            try :
                textData = f.read()
            except:
                logger.exception("Could not load %s" % filePath + " ", traceback.format_exc())
                continue
            f.close()
            wakati_text.append(wakati(textData))

    wakati_text_file = config.get("word2vec", "wakati.file.path")
    f = open(wakati_text_file, 'w', encoding='utf-8-sig')
    f.write('\n'.join(wakati_text))
    f.close()



if __name__ == "__main__":
    logger.debug("Start wakatigaki")

    text_to_wakati()

    logger.debug("End wakatigaki")