# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 20:57:56 2020

@author: Abhishek
"""

import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
#from nltk.stem.porter import PorterStemmer
import nltk.data
from sklearn import preprocessing
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

#nltk.download()



ds=pd.read_csv("thepopo-processed.csv",)

df = pd.DataFrame(ds)
print(df)

#df=df.sample(frac=1)




print(df.Sentiment)
le = preprocessing.LabelEncoder()
df['Sentiment'] = le.fit_transform(df.Sentiment.values)
print(df.Sentiment)

df=df.sample(frac=1)

X_tr = df.loc[:2000, 'processed'].values
y_train = df.loc[:2000, 'Sentiment'].values
X_te = df.loc[2001:, 'processed'].values
y_test = df.loc[2001:, 'Sentiment'].values


from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()

X_train = vectorizer.fit_transform(X_tr)
X_test = vectorizer.transform(X_te)


import pickle
pickle.dump(vectorizer, open("vectorizer.pickle", "wb"))
#pickle.dump(selector, open("selector.pickle", "wb"))

#print(train_vectors.shape, test_vectors.shape)


#Create a svm Classifier
clf = svm.SVC(kernel='linear') # Linear Kernel

#Train the model using the training sets
clf.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)
print(y_pred)

import pickle
with open('model_pickle','wb')as f:
    pickle.dump(clf,f)
    

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


#print("Precision:",metrics.precision_score(y_test, y_pred))


# Model Recall: what percentage of positive tuples are labelled as such?
#print("Recall:",metrics.recall_score(y_test, y_pred))







