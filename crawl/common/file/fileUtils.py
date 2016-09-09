#!/usr/bin/env python
# coding: utf-8
"""
ファイル列操作処理
"""
import os
import re
from common.log import logging
logger = logging.getLogger("")


def remove_file(file):
    '''
    ファイルを削除する（ファイル存在有無チェック後）
    '''
    if os.path.exists(file):
        os.remove(file)

def makedirs(dir):
    '''
    ディレクトリを作成する（ディレクトリ存在有無チェック後）
    '''
    if not os.path.isdir(dir):
        os.makedirs(dir)