# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python [conda env:ds] *
#     language: python
#     name: conda-env-ds-py
# ---

# load dependency libraries
import math
from statistics import mode 
import os
import copy
# import operator
# import string
# from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pickle

# +
N = 3001

# extracting english stop words
stop_words = stopwords.words('english')

# Initializing Porter Stemmer object
st = PorterStemmer()

# folder to store pickel files
pickle_folder = "./PickleFiles/"
os.makedirs(pickle_folder, exist_ok=True)
# -

with open(pickle_folder + 'inverted_index.pickle', 'rb') as f:
    inverted_index=pickle.load(f)                   # rename 

with open(pickle_folder + 'webpages_tokens.pickle', 'rb') as f:
    webpages_tokens =pickle.load(f)                   # rename 

# +
# computing idf of each token

# df = {}
idf = {}

for key in inverted_index.keys():
    df = len(inverted_index[key].keys())
    idf[key] = math.log2(N/df)

# +
# doc_length = {}
# for page in webpages_tokens:
    
#     doc_length[page] = 

# +
max_freq = {}

for page in webpages_tokens:
    most_freq_token = mode(webpages_tokens[page])
    max_freq[page] = inverted_index[most_freq_token][page]
    

# +
# function to compute tf-idf of each token

# making a temporary copy of the inverted index
tf_idf = copy.deepcopy(inverted_index)

# def calculate_tfidf(token, webpage):
for token in tf_idf:
    for page in tf_idf[token]:
        tf = tf_idf[token][page] / max_freq[page]
        tf_idf[token][page] = tf * idf[token]
# -





