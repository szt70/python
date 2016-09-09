#!/usr/bin/env python
# coding: utf-8
"""
設定ファイルに関する初期処理
"""

import os.path
import configparser
from common.log import logging
logger = logging.getLogger("")

script_dir = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(script_dir, "config.ini")

class ConfigUtil():

    def __init__(self):
        if not os.path.exists(config_file) :
            logger.error(" not exsit config file : {0} ".format(config_file))
        else :
            logger.debug("config read ... {0} ".format(config_file))
            self.config = configparser.SafeConfigParser()
            self.config.read(config_file, encoding='utf-8-sig')
            print(self.config.get("test", "key"))

_configUtil = ConfigUtil()

def get(section, key):
    return _configUtil.config.get(section, key)
