import collections
import math
import MeCab
import traceback
import logging

#logger
logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)
log_fmt = '[%(asctime)s] %(levelname)s - %(filename)s#%(funcName)s:%(lineno)d: %(message)s'
logging.basicConfig(format=log_fmt)

tagger = MeCab.Tagger("-u /usr/local/lib/mecab/dic/mecab-user-dict-seed.20160915.dic")
taggerPart = MeCab.Tagger("-Owakati -u /usr/local/lib/mecab/dic/mecab-user-dict-seed.20160915.dic")

def mostFrequentWords(file, num):
  words = collections.Counter()

  f = open(file)
  line = f.readline()
  while line:
    parse_line = tagger.parse(line)
    print("line----------" + line)
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

      print("node[1]----------" + node[1])      
      print("w=" + part_word + "p=" + part + "ps=" + part_sub)

    line = f.readline()
  return words.most_common(num)

p_cls = {}
p_word = {}

def train(cls, vocabulary, documents):

  # 各訓練文書の件数
  n_cls = {}
  total = 0.0
  for c in cls:
    n_cls[c] = len(documents[c])
    total += n_cls[c]

  # 各訓練文書の生起確率
  for c in cls:
    p_cls[c] = n_cls[c] / total

  # 各クラス毎の単語の生起回数
  n_word = {}
  for c in cls:
    n_word[c] = {}
    for d in documents[c]:
      for word in vocabulary:
        if word in d:
          if not word in n_word[c]:
            n_word[c] = collections.Counter()
          n_word[c][word] += 1

  # 各クラス毎の単語の生起確率
  for c in cls:
    p_word[c] = {}
    for word in vocabulary:
      p_word[c][word] = (n_word[c][word] + 1) / (n_cls[c] + 2)

def classify(data):
  # 各クラス毎にlogP(D)を求める
  pp = {}
  for c in cls:
    pp[c] = math.log(p_cls[c])
    for word in vocabulary:
      if word in data:
        pp[c] += math.log(p_word[c][word])

      else:
        pp[c] += math.log((1 - p_word[c][word]))

  # 求めたlogP(D)の内、どれが最も大きいか判定
  for c in cls:
    maxpp = maxpp if 'maxpp' in locals() else pp[c]
    maxcls = maxcls if 'maxcls' in locals() else c

    if maxpp < pp[c]:
      maxpp = pp[c]
      maxcls =c

  return (maxcls, maxpp)

def bags_of_words(file):
  # 各ツイートを品詞分解した２次元配列を返します
  tweet_wakata = []
  f = open(file)
  line = f.readline()
  while line:
    nodes = taggerPart.parse(line)
    wakati = []
    for node in nodes.split(" "):
      wakati.append(node)
    tweet_wakata.append(wakati)
    line = f.readline()

  return tweet_wakata

def test(data, label):
  '''
  dataがlabelである確率を返す
  '''
  i = 0.0
  for tweet in data:
    if classify(tweet)[0] == label:
      i += 1
  return (i / len(data))

cls = ["mottoatuku", "ichirosbot"]

words = {} 
words["mottoatuku"] = mostFrequentWords("tweet_mottoatuku.txt", 5)
words["ichirosbot"] = mostFrequentWords("tweet_ichirosbot.txt", 5)

documents = {}
documents["mottoatuku"] = bags_of_words("mottoatuku_150.txt")
documents["ichirosbot"] =  bags_of_words("ichirosbot_150.txt")

tpl = words["mottoatuku"] + words["ichirosbot"]
vocabulary = set([])
for word in tpl:
  vocabulary.add(word[0])

train(cls, vocabulary, documents)

result = test(bags_of_words("mottoatuku_50.txt"), "mottoatuku")
print(result)

result = test(bags_of_words("mottoatuku_50.txt"), "ichirosbot")
print(result)
