from gensim import models

sentence = models.doc2vec.LabeledSentence(
    words=[u'so`bme', u'words', u'here'], tags=["SENT_0"])
sentence1 = models.doc2vec.LabeledSentence(
    words=[u'here', u'we', u'go'], tags=["SENT_1"])
sentence2 = models.doc2vec.LabeledSentence(
    words=[u'test', u'test', u'human'], tags=["SENT_2"])
sentence3 = models.doc2vec.LabeledSentence(                                                                                                                                                                           
    words=[u'abc', u'test', u'pc'], tags=["SENT_3"])  

sentences = [sentence, sentence1, sentence2, sentence3]

class LabeledLineSentence(object):
    def __init__(self, filename):
        self.filename = filename
    def __iter__(self):
        for uid, line in enumerate(open(filename)):
            yield LabeledSentence(words=line.split(), labels=['SENT_%s' % uid])
            
model = models.Doc2Vec(alpha=.025, min_alpha=.025, min_count=1)
model.build_vocab(sentences)

for epoch in range(10):
    model.train(sentences)
    model.alpha -= 0.002  # decrease the learning rate`
    model.min_alpha = model.alpha  # fix the learning rate, no decay

model.save("my_model.doc2vec")
model_loaded = models.Doc2Vec.load('my_model.doc2vec')

# ある文書に似ている文書を表示
print (model.docvecs.most_similar(["SENT_0"]) )
print (model.docvecs.most_similar(["SENT_3"]) )

print (model_loaded.docvecs.most_similar(["SENT_1"]) )

print (model.similar_by_word("test"))
print( model.most_similar_words('test'))

