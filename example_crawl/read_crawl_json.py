'''
Created on 2016/11/03

@author: XXX

@desc:
        scrapyでクロールしたスクレイピング結果jsonlineファイルを読み込み
'''
import json

if __name__ == '__main__':
    jsonfile = "/tmp/export.json"
    with open(jsonfile, encoding="utf-8") as f:
        line = f.readline()
        while line != '':
            jsonData = json.loads(line)
            print("url={0}, title={1}".format(jsonData['url'], jsonData['title']))
            line = f.readline()