#!/usr/bin/env python
# coding:utf-8
'''
    word2vec利用
'''

import sys
import re
import os
import traceback
import json
import urllib
import yaml

import word2vec
import config
from common.lang import stringUtils
from common.log import logging
logger = logging.getLogger("test")
wakati_bin_file = config.get("word2vec", "word2vec.bin.path")

def preprocess():
    wakati_text_file = config.get("word2vec", "wakati.file.path")
    word2vec.word2vec(wakati_text_file, wakati_bin_file, size=300, verbose=True)

# 入力された単語から近い単語をn個表示する
def s(posi, nega=[], n=10):
    cnt = 1 # 表示した単語の個数カウント用
    # 学習済みモデルからcos距離が最も近い単語n個(topn個)を表示する
    result = model.most_similar(positive = posi, negative = nega, topn = n)
    for r in result:
        print (cnt,'　', r[0],'　', r[1])
        cnt += 1


def echo(label, tlist):
    print ("==============================")
    print (label)
    print ('------------------------------')
    for x in tlist:
        print (x[0], x[1])

if __name__ == "__main__":

    # run only onece
    preprocess()

    model = word2vec.load(wakati_bin_file)

    key = u'ライフ'
    print (model.cosine(key))
    tlist = model.cosine(key)
    echo(key, tlist)

    key = 'ブラジル'
    tlist = model.cosine(key)
    echo(key, tlist)