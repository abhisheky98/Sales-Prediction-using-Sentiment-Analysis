# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 20:57:56 2020

@author: Abhishek
"""

#Code for creating processed file

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



ds=pd.read_csv("thepopo.csv",)

df = pd.DataFrame(ds)

exclude = set(string.punctuation)
def remove_punctuation(x):
    """
    Helper function to remove punctuation from a string
    x: any string
    """
    try:
        x = ''.join(ch for ch in x if ch not in exclude)
    except:
        pass
    return x
# Apply the function to the DataFrame
df.Review = df.Review.apply(remove_punctuation)
#print('Review')
#print(df.Review)




df['Review'] = df['Review'].str.lower()



def identify_tokens(row):
    Review = row['Review']
    tokens = nltk.word_tokenize(Review)
   # taken only words (not punctuation)
    token_words = [w for w in tokens if w.isalpha()]
    return token_words

df['words'] = df.apply(identify_tokens, axis=1)





stops = set(stopwords.words("english"))                  

def remove_stops(row):
    my_list = row['words']
    meaningful_words = [w for w in my_list if not w in stops]
    return (meaningful_words)

df['Review1'] = df.apply(remove_stops, axis=1)


print(df.Review)





def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def pos(row):
    my_list=row['Review1']

    a=[get_wordnet_pos(word) for word in my_list]

    return(a)


df['pos_tagged'] = df.apply(pos, axis=1)
print(df.pos_tagged)



def lema(row):
    lemming=WordNetLemmatizer()
    #print("-----------------test-----------------")
    my_list=row['Review1']
    my_pos=row['pos_tagged']
    lemming_list=[lemming.lemmatize(w,p)for (w,p) in zip(my_list,my_pos)]
    return (lemming_list)
df['lemmatized_words'] = df.apply(lema, axis=1)



def rejoin_words(row):
    my_list = row['lemmatized_words']
    joined_words = ( " ".join(my_list))
    return joined_words

df['processed'] = df.apply(rejoin_words, axis=1)







df.to_csv('thepopo-processed.csv', index=False)





