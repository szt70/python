#!/usr/bin/env python
# coding: utf-8
"""
文字列操作処理
"""
import os
import re
from common.log import logging
logger = logging.getLogger("")


def collect_line_break(text):
    '''
    改行をまとめる
    '''
    return re.sub(r'\n+', '\n', text)

def removeHalfSymbol(text):
    '''
    半角記号を削除する
    '''
    str = text.rstrip()
    str = re.sub(re.compile("[!-/:-@[-`{-~]"), '', str)
    return str

def removeControlCharacter(s):
    '''
    制御文字を削除する
    '''

    ret = ''
    for c in s:
        ord_num = ord(c)

        #制御文字
        if(ord_num <= 31):
            a = 1234

        else:
            ret += c

    return ret