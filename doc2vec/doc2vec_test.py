import gensim

sentences = [
    ['human', 'interface', 'computer'], #0
    ['survey', 'user', 'computer', 'system', 'response', 'time'], #1
    ['eps', 'user', 'interface', 'system'], #2
    ['system', 'human', 'system', 'eps'], #3
    ['user', 'response', 'time'], #4
    ['trees'], #5
    ['graph', 'trees'], #6
    ['graph', 'minors', 'trees'], #7
    ['graph', 'minors', 'survey'] #8
]


docs = [
    ['human', 'interface', 'computer'], #0
    ['survey', 'user', 'computer', 'system', 'response', 'time'], #1
    ['eps', 'user', 'interface', 'system'], #2
    ['system', 'human', 'system', 'eps'], #3
    ['user', 'response', 'time'], #4
    ['trees'], #5
    ['graph', 'trees'], #6
    ['graph', 'minors', 'trees'], #7
    ['graph', 'minors', 'survey'] #8
]

titles = [
    "doc1",
    "doc2",
    "doc3",
    "doc4",
    "doc5",
    "doc6",
    "doc7",
    "doc8",
    "doc9"
]

labeledSentences = gensim.models.doc2vec.LabeledListSentence(sentences)
#labeledSentences = gensim.models.doc2vec.LabeledListSentence(docs,titles)
model = gensim.models.doc2vec.Doc2Vec(labeledSentences, min_count=0)

# ラベル一覧を取得
print("-------------------------------------") 
print (model.labels)

# ある文書に似ている文書を表示
print("-------------------------------------")
print( model.most_similar_labels('SENT_0') )
#print( model.most_similar_labels('SENT_doc1'))

# ある文書に似ている単語を表示
print("-------------------------------------") 
print( model.most_similar_words('human'))
#print( model.most_similar_words('SENT_doc1'))

# 複数の文書を加算減算した上で、似ているユーザーを表示
print("-------------------------------------") 
print( model.most_similar_labels(positive=['SENT_1', 'SENT_2'], negative=['SENT_3'], topn=5))

# 複数の文書を加算減算した上で、似ている単語を表示
print("-------------------------------------") 
print( model.most_similar_words(positive=['SENT_1', 'SENT_2'], negative=['SENT_3'], topn=5))
