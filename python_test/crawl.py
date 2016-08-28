#!/usr/bin/env python
# coding:utf-8

import sys
import os
import traceback
import json
import urllib
import yaml
from bs4 import BeautifulSoup 
from lib2to3.pgen2 import driver
from selenium import webdriver
from urllib.parse import urljoin
from logging import config,getLogger
config.dictConfig(yaml.load(open("logging.conf", encoding='UTF-8').read()))
logger = getLogger("test")

def crawl(pages, depth=2):
    setpages = set()

    for i in range(depth):
        newpages = set()
        for page in pages:
            try:
                c = scraping(page)
                soup = BeautifulSoup(c, "lxml")
            except:
                logger.error("Could not open %s" % page + " " + traceback.format_exc())
                continue

            setpages.add(page)

            links = soup('a')
            for link in links:
                if ('href' in dict(link.attrs)):
                    url = urljoin(page, link['href'])
                    if url.find("'") != -1: continue
                    url = url.split('#')[0]
                    if url[0:4] == 'http' and not url in setpages:
                        newpages.add(url)
            logger.debug("get link : %d" % len(links))
        pages = newpages

    return list(setpages)


def scraping(url):
    """スクレイピング
    """

    log_name = "/tmp/phantomjs.log"
    userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"
    driver = webdriver.PhantomJS(
        desired_capabilities={
            'phantomjs.page.settings.userAgent': userAgent,
        },
        service_log_path=log_name
                                 )
    f = open("c:/tmp/cookie.json")
    cookieList = json.load(f)

    for c in cookieList:
        driver.add_cookie(c)
    driver.get(url)
    html = driver.page_source
    logger.debug('success scraping : ' + url)
    return html


if __name__ == "__main__":
    urls = ["http://news.yahoo.co.jp/"]

    pages = crawl(urls)
    print("crawl count : " + len(pages.count))

    f = open("c:/tmp/crawlurls.json", "w")
    json.dump(pages, f)
    f.close()