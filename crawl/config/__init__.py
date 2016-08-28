import configparser
import yaml
from logging import config
import logging
DEFAULT_CONFIG_FILE = "./config.ini"
LOGGING_CONFIG_FILE = "logging.conf"

config.dictConfig(yaml.load(open(LOGGING_CONFIG_FILE, encoding='UTF-8').read()))
loggerDefault = logging.getLogger("")

class ConfigUtil():
    def __init__(self):
        loggerDefault.debug("config read ... {0} {1} ".format(DEFAULT_CONFIG_FILE, LOGGING_CONFIG_FILE))
        #self.config = ConfigParser.SafeConfigParser()
        self.config.read(DEFAULT_CONFIG_FILE)


#_util = ConfigUtil()

def getLogger(loggerName):
    return logging.getLogger(loggerName)

#def get(section, key):
#    return _util.config.get(section, key)
