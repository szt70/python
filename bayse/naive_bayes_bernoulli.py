import re
import numpy
from sklearn.externals import joblib
from sklearn.naive_bayes import BernoulliNB
from gensim import corpora, matutils
import collections
import MeCab

tagger = MeCab.Tagger("-u /usr/local/lib/mecab/dic/mecab-user-dict-seed.20160915.dic")
taggerPart = MeCab.Tagger("-Owakati -u /usr/local/lib/mecab/dic/mecab-user-dict-seed.20160915.dic")



def bags_of_words(file):
  '''
     各ツイートを品詞分解した２次元配列を返します
    @param      file ... 1行が1ツイートの文章    
    @return      各ツイート文章の単語の2次元配列
    [      ["ＷＢＣ", "バット", "甲子園"]      ["ＷＢＣ", "バット", "甲子園"]      ["ＷＢＣ", "バット", "甲子園"]    ]
  '''
  tweet_wakata = []
  f = open(file)
  line = f.readline()
  while line:
    wakati = []
    parse_line = tagger.parse(remove_url(line))
    #改行や非自立語等、特徴の無い単語は除外
    for nodes in parse_line.split('\n'):
      node = nodes.split('\t')
      part_word = node[0]
      if part_word == "EOS":
        continue
      if len(part_word) == 0:
        continue
      part = node[1].split(',')[0]
      part_sub = node[1].split(',')[1]
      if part_sub == "非自立" or part_sub == "サ変接続" or part_sub == "代名詞":
        continue
      elif part == "名詞" and len(part_word) == 1:
        continue
      elif part == "助詞" or part == "記号" or part == "助動詞" or part == "連体詞":
        continue
      elif not part == "名詞":
        continue

      wakati.append(part_word)
      #print(part_word + " -----> " + node[1])

    tweet_wakata.append(wakati)
    line = f.readline()

  return tweet_wakata

def mostFrequentWords(file, num):
  '''
  頻出単語を取得
  @param   file ... 1行が1ツイートの文章    
  @param   num ...  上位何件を取得するか  
  '''
  words = collections.Counter()

  f = open(file)
  line = f.readline()
  while line:
    parse_line = tagger.parse(remove_url(line))
    print("parse_line : {0}".format(parse_line))
    for nodes in parse_line.split('\n'):
      node = nodes.split('\t')
      part_word = node[0]
      if part_word == "EOS":
        continue
      if len(part_word) == 0:
        continue
      part = node[1].split(',')[0]
      part_sub = node[1].split(',')[1]

      if part_sub == "非自立" or part_sub == "サ変接続" or part_sub == "代名詞":
        continue
      elif part == "名詞":
        words[part_word] += 1
      elif part == "名詞" and len(part_word) == 1:
        continue
      elif part == "助詞" or part == "記号" or part == "助動詞" or part == "連体詞":
        continue
      elif part == "形容詞":
        words[part_word] += 1
      elif not part == "名詞":
        continue

      #print("w=" + part_word + "p=" + part + "ps=" + part_sub)

    line = f.readline()
  return words.most_common(num)

def remove_url(text):
  '''
  文字列からURLを削除
  '''
  return re.sub(r"http[s]?://[a-zA-Z0-9.\/?=&_%;\-$]*", "", text)


def label_put(cls, dense):
  '''  
  単語の疎行列にクラス名のラベルを貼る（配列番号でマッチさせる）
  ラベルの配列と疎行列の配列数は同じとなる。
  return[0] ... ラベルの配列
  return[1] ... 単語の祖行列
  '''
  label = []
  array = []
  for c in cls:
    for cps in dense[c]:
      #print("label_put{0} : {1}".format(c, cps))
      array.append(cps)
      label.append(c)
  return label, array

def train(cls, docments):
  '''
  訓練データを元に教師データを作成
  cls ... クラス名の配列
  docments ... bag of wordsの2次元配列
  '''
  docments_all = []
  for c in cls:
    docments_all = docments_all + docments[c]
    #print("documents[{0}] {1} : {2}".format(c, len(docments[c]), docments[c]))
  
  #print("documents[ALL] {0} : {1}".format(len(docments_all), docments_all))

  #dictionary作成
  dictionary = corpora.Dictionary(docments_all)
  dictionary.save('vocabulary.dict')
  print("dictionary {1} : {2}".format(c, len(dictionary.token2id),  dictionary.token2id))

  #dense作成
  dense = {}
  for c in cls:
    corpus = [dictionary.doc2bow(text) for text in docments[c]]
    #print("corpus[{0}] {1}: {2}".format(c, len(corpus), corpus) )
    dense_list = list()
    d_list = matutils.corpus2dense(corpus, num_terms=len(dictionary))

    #文書数ループ
    for i in range(0, len(corpus)):
      dense_list.append(d_list.T[i].tolist())
      #print("dense[{0}] {1}: {2}".format(c, len(dense_list[i]), dense_list[i]) )
    dense[c] = dense_list

  train_data = label_put(cls, dense)
  label_train =  train_data[0]
  array_train =  train_data[1]
  #print("label {0}: {1}".format(len(label), label)) 
  #print("data {0}: {1}".format(len(data), data))
  clf = BernoulliNB()
  clf.fit(array_train, label_train)

  #モデルの保存
  joblib.dump(clf,"BernoulliNB.model")


if __name__ == "__main__":

  cls = ["TigersDreamlink", "kansai_noodle"]

  #頻出単語取得
  vocabulary = {}
  for c in cls:
    vocabulary[c] =  mostFrequentWords("tweet_" + c + ".txt", 5)
    print("mostFrequentWords: {0}".format(vocabulary[c]))

  #訓練用データ文章を分かち書きの配列で取得
  docments = {}
  docments_all = []
  for c in cls:
    docments[c] = bags_of_words("tweet_" + c + ".txt")

  #教師データ作成
  train(cls, docments)

  #辞書とモデルの読み込み
  dictionary = corpora.Dictionary.load('vocabulary.dict')
  model = joblib.load("BernoulliNB.model")

  #テストデータを識別
  docments_t = bags_of_words("test.txt")
  print("docments_t : {0}".format(docments_t))
  corpus_t = [dictionary.doc2bow(text) for text in docments_t]
  print("corpus_t : {0}".format(corpus_t))
  dense_t = matutils.corpus2dense(corpus_t, num_terms=len(dictionary)).T[0]

  print("dense_t : {0}".format(dense_t))

  print( model.predict(dense_t) )
