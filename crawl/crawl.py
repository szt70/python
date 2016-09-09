#!/usr/bin/env python
# coding:utf-8

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
import config
from common.log import logging
logger = logging.getLogger("test")

def crawl(pages, depth=2):
    setpages = set()
    sobj = Scraping()
    parse = htmlPerser.HTMLParser();
    for i in range(depth):
        newpages = set()
        for page in pages:
            try:
                html = sobj.scraping(page)
                parseResult = parse.get(page, html)
                # output
                md5 = hashlib.md5(page.encode('utf-8')).hexdigest()
                output = {"html": str(parseResult), "date": datetime.now().strftime('%Y/%m/%d %H:%M:%S'), "md5": md5, "url": page}
                dir = config.get("crawl", "crawldata.dir.path")
                if not os.path.exists(dir):
                    os.makedirs(dir)
                filepath = dir + md5 + ".json";
                # write the output as a json file
                with open(filepath, "w", encoding='utf-8-sig') as fout:
                    json.dump(output, fout, ensure_ascii=False, indent=4, sort_keys=True)
                soup = BeautifulSoup(html, "lxml")
            except:
                logger.exception("Could not open %s" % page + " ", traceback.format_exc())
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
            logger.debug("(depth={0}) get link : {1}".format( i, len(links)) )
        pages = newpages

    return list(setpages)


if __name__ == "__main__":
    logger.debug("Start crawl")
    urls = ["http://news.yahoo.co.jp/"]

    pages = crawl(urls)
    logger.debug("crawl get url count : {0}".format(len(pages)))

    f = open("c:/tmp/crawlurls.json", "w")
    json.dump(pages, f)
    f.close()
    logger.debug("End crawl")