import numpy as np
from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB

X = np.array([[1,2,3,4,5,6,7,8],
              [1,1,3,4,5,6,6,7],
              [2,1,2,4,5,8,8,8]]) # 特徴ベクトル
y = np.array([1, 2, 3]) # そのラベル

#パラメータを設定
#alpha .... float, optional -> スムージングparameter(defaultは1.0)
#class_prior .... array-like, size=[n_classes] -> Prior probabilities of the classes
#                 クラスの事前確率。指定された場合は事前確率は、データに応じて調整されていません
#fit_prior .... boolean -> class prior probabilitiesを使うかどうか
#               クラス事前確率を学習するかどうかをブール値。
#                falseの場合、均一の事前確率が使用されます。
clf = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
clf.fit(X, y)

#モデルの保存
joblib.dump(clf,"MultinomialNB.model")

#モデルの読み込み
model = joblib.load("MultinomialNB.model")

t = np.array( [[2,2,4,5,6,8,8,8]] ) # テストデータ

print( model.predict(t) )
print( model.predict_log_proba(t) )
