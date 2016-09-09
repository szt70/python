# -*- coding: utf-8 -*-
import MeCab
import sys
import codecs

f = open('c:/tmp/in.txt','r', encoding='utf-8-sig')
text = f.read()
f.close()

m = MeCab.Tagger("-Owakati")
print("-Owakati:" + m.parse(text))
print("------")
m = MeCab.Tagger("-Odump")
print("-Odump:" + m.parse(text))

