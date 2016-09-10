from gensim.models import word2vec
# 学習
sentences = word2vec.Text8Corpus("corpus_wakati.txt")
model = word2vec.Word2Vec(sentences, size=100)
# モデルの保存と読込
model.save("sample.model")


