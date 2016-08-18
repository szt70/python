#!/usr/bin/env python
# coding: utf-8
"""
スクレイピング
"""
__author__ = "szt70"
__version__ = "0.0.1"
__date__    = "2016-08-18"

import sys
import json
import os
from lib2to3.pgen2 import driver

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def scraping_requests(url, output_name):
    """ requests利用してスクレイピング
    """

    # get a HTML response
    response = requests.get(url)
    html = response.text.encode(response.encoding)  # prevent encoding errors
    # parse the response
    soup = BeautifulSoup(html, "lxml")
    # extract
    ## title
    header = soup.find("head")
    title = header.find("title").text
    print("title: " + title)
    # description
    description = header.find("meta", attrs={"name": "description"})
    description_content = description.attrs['content']
    body = soup.find("body").text
    # output
    output = {"title": title, "description": description_content, "body": body}
    # write the output as a json file
    with open(output_name, "w") as fout:
        json.dump(output, fout, ensure_ascii=False, indent=4, sort_keys=True)


def scraping(url, output_name):
    """ ユーザーエージェント、Cookieを設定してスクレイピング
    """
    log_name = "/tmp/phantomjs.log" #ログを出力しない場合はos.path.devnull
    userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53"
    driver = webdriver.PhantomJS(
        desired_capabilities={
            'phantomjs.page.settings.userAgent': userAgent,
        },
        service_log_path=log_name
                                 )
    #JSON形式のファイルからCookie読み込み
    f = open("c:/tmp/cookie.json")
    cookieList = json.load(f)

    for c in cookieList:
        driver.add_cookie(c)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    header = soup.find("head")
    title = header.find("title").text
    print(title)
    description = header.find("meta", attrs={"name": "description"})
    description_content = description.attrs['content']
    body = soup.find("body").text

    #body, description, titleをファイル出力
    output = {"title": title, "description": description_content, "body": body}
    with open(output_name, "w") as fout:
        json.dump(output, fout, ensure_ascii=False, indent=4, sort_keys=True)

#
#
#
if __name__ == '__main__':
    print(sys.argv)
    # arguments
    argvs = sys.argv
    ## check
    if len(argvs) != 3:
        print ("Usage:  [url] [outputPath]")
        exit()
    url = argvs[1]
    output_name = argvs[2]

    scraping(url, output_name)