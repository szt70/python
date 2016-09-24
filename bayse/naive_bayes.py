'''
  ナイーブベイズ識別器
  2つのカテゴリのツイート150件ずつのファイルを読み込み訓練語、テストデータのカテゴリを識別する

'''
import math
import sys
from collections import defaultdict
import MeCab

tagger = MeCab.Tagger("-u /usr/local/lib/mecab/dic/mecab-user-dict-seed.20160915.dic")
taggerPart = MeCab.Tagger("-Owakati -u /usr/local/lib/mecab/dic/mecab-user-dict-seed.20160915.dic")

class NaiveBayes:
    """Multinomial Naive Bayes"""
    def __init__(self):
        self.categories = set()     # カテゴリの集合
        self.vocabularies = set()   # 文書全体の単語(ボキャブラリ)
        self.wordcount = {}         # wordcount[cat][word] カテゴリでの単語の出現回数
        self.catcount = {}          # catcount[cat] カテゴリの出現回数 = P(Ci)＝事前確率
        self.denominator = {}       # denominator[cat] P(word|cat)の分母の値
    
    def train(self, cls, data):
        """ナイーブベイズ分類器の訓練"""
        # カテゴリを抽出して辞書を初期化
        for c in cls:
            self.categories.add(c)
        for cat in self.categories:
            self.wordcount[cat] = defaultdict(int)
            self.catcount[cat] = 0

        # 文書集合から
        # カテゴリをカウントし事前確率を取得、
        # 各カテゴリで単語をカウント（後程、単語の条件付き確率の分子で利用する）
        for c in cls:
            for doc in data[c]:
                self.catcount[c] += 1
                for word in doc:
                    self.vocabularies.add(word)
                    self.wordcount[c][word] += 1
                    #print("wordcount[{0}][{1}] : {2} ".format(c, word, self.wordcount[c][word]))

        # 単語の条件付き確率の分母の値をあらかじめ一括計算しておく（高速化のため）
        for cat in self.categories:
            #print("denominator : {0} {1} ".format(cat, self.wordcount[cat].values()))
            self.denominator[cat] = sum(self.wordcount[cat].values()) + len(self.vocabularies)
    
    def classify(self, doc):
        """事後確率の対数 log(P(cat|doc)) がもっとも大きなカテゴリを返す"""
        best = None
        max = -sys.maxsize
        for cat in self.catcount.keys():
            p = self.score(doc, cat)
            if p > max:
                max = p
                best = cat
        return best
    
    def wordProb(self, word, cat):
        """単語の条件付き確率 P(word|cat) を求める"""
        # ラプラススムージングを適用(+1してる)
        # wordcount[cat]はdefaultdict(int)なのでカテゴリに存在しなかった単語はデフォルトの0を返す
        # 分母はtrain()の最後で一括計算済み
        print("{0} {1} : {2} ".format(cat , word, self.wordcount[cat][word]))
        return float(self.wordcount[cat][word] + 1) / float(self.denominator[cat])
    
    def score(self, doc, cat):
        """文書が与えられたときのカテゴリの事後確率の対数 log(P(cat|doc)) を求める"""
        total = sum(self.catcount.values())  # 総文書数
        score = math.log(float(self.catcount[cat]) / total)  # log P(cat)
        for word in doc:
            #全ての単語の条件付き確率を乗算してスコアを求めるが、かけ算部分がアンダーフローを起こす可能性がある。そこで、対数をとってかけ算を足し算化
            # logをとるとかけ算は足し算になる
            score += math.log(self.wordProb(word, cat))  # log P(word|cat)
        return score
    
    def __str__(self):
        #print(self.vocabularies)
        total = sum(self.catcount.values())  # 総文書数
        return "documents: %d, vocabularies: %d, categories: %d" % (total, len(self.vocabularies), len(self.categories))

def bags_of_words(file):
  ''' 
    各ツイートを品詞分解した２次元配列を返します
    @param
      file ... 1行が1ツイートの文章

    @return
      各ツイート文章の単語の2次元配列
    [
      ["ＷＢＣ", "バット", "甲子園"]
      ["ＷＢＣ", "バット", "甲子園"]
      ["ＷＢＣ", "バット", "甲子園"]
    ]
  '''
  tweet_wakata = []
  f = open(file)
  line = f.readline()
  while line:
    wakati = []
    parse_line = tagger.parse(line)
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

      wakati.append(part_word)
      print(part_word + " -----> " + node[1])

    tweet_wakata.append(wakati)
    line = f.readline()

  return tweet_wakata


if __name__ == "__main__":

    # カテゴリを定義
    cls = ["mottoatuku", "ichirosbot"]

    # 各文書（ツイート）の単語を取得しカテゴリを設定
    documents = {}
    documents["mottoatuku"] = bags_of_words("mottoatuku_150.txt")
    documents["ichirosbot"] =  bags_of_words("ichirosbot_150.txt")

    # ナイーブベイズ分類器を訓練
    nb = NaiveBayes()
    nb.train(cls, documents)
    print (nb)

    #各カテゴリでの単語の条件付き確率を求める（内部動作確認の為の用処理、実際は不要）
    words = ["ＷＢＣ", "バット", "甲子園", "Chinese"]
    for c in cls:
        for word in words:
            print ("P({0}|{1}) = {2}".format( word, c, nb.wordProb(word, c) ))
    
    # テストデータのカテゴリを予測
    test = ["ＷＢＣ", "バット", "甲子園", "自分"] 
    for c in cls:
        print ("log P({0}|{1}) = {2}".format( test, c, nb.score(test, c)) )
    print (nb.classify(test))
