import sys
import time
from gensim.models import word2vec

argvs = sys.argv
if len(argvs) < 2:
  print ("Usage:  [word1] [wore2]")
  exit()

word1 = argvs[0]
word2 = argvs[1]

def load_model():
  global model
  timeStart = time.clock();
  model = word2vec.Word2Vec.load("sample.model")
  timeTotal = round(time.clock() - timeStart, 3)
  print("load model ... {0}s".format(timeTotal))

def print_result(out):
  print("-----")
  for x in out:
    for y in x:
      try:
        print (y, '\t')
      except KeyError:
        print("not found : " + y)

try:
  load_model()
  #よく一緒に使われる(距離が近い)単語を3つ取得
  out = model.most_similar(positive=[u'ピカチュウ'], topn=3)
  print_result(out)
  #単語を足して、それらとよく使われる単語を取得
  out = model.most_similar(positive=[u'ピカチュウ', u'進化'], topn=5)
  print_result(out)
  #単語から単語を引いた意味を取得
  out = model.most_similar(positive=[u'ピカチュウ', u'モンスター'], negative=[u'ポケモン'], topn=5)
  print_result(out)

  #単語の件数と一覧
  print ("key list-----------------------------")
  print("key count : {0}".format( len(model.vocab.keys())) )
  #print (model.vocab.keys()) #件数多いと要注意
 
  #単語のベクトルを取得
  print("ベクトル---------------------------------")
  print (model[u'ピカチュウ'])

  #類似度計算
  for nation in [u"学校", u"サトシ", u"ピチュー", u"ゲーム", u"ポケモン"]:
    result = model.similarity(u"ピカチュウ", nation)
    print("類似度計算結果 : ", nation, " = ", result)

except KeyError:
  print ("存在しないキーワードです。" + word1)
