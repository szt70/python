#!/usr/bin/env python
# coding: utf-8
"""
ロギング処理
"""
import os
import yaml
from logging import config
import logging
script_dir = os.path.abspath(os.path.dirname(__file__))
logging_config_file = os.path.join(script_dir, "logging.yml")

def getLogger(loggerName):
    '''
    loggerを取得
    '''
    return logging.getLogger(loggerName)

if not os.path.exists(logging_config_file) :
    logger.error(" not exsit config file : {0} ".format(logging_config_file))
else :
    config.dictConfig(yaml.load(open(logging_config_file, encoding='UTF-8').read()))
    getLogger("").debug("loggin config read ... {0} ".format( logging_config_file))
