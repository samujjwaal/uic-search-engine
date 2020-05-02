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

# # Preprocess Docs
#

# load dependency libraries
import os
import re
import pickle
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# +
# extracting english stop words
stop_words = stopwords.words('english')

# Initializing Porter Stemmer object
st = PorterStemmer()

# Initializing regex to remove words with one or two characters length
# shortword = re.compile(r'\W*\b\w{1,2}\b')

# folder to store pickel files
pickle_folder = "./PickleFiles/"
os.makedirs(pickle_folder, exist_ok=True)

# +
pages_folder = "./FetchedPages/"
filenames = os.listdir(pages_folder)

# list to store filenames of all stored crawled webpages
files = []

for name in filenames:
    files.append(name)

# len(files)

# +
# for file in files[:1]:
#     web_page = open(pages_folder + file, "r", encoding="utf-8")
#     code = web_page.read()
# #     print(code)
#     soup = BeautifulSoup(code, "html.parser")
#     [s.extract() for s in soup(['style', 'script', '[document]', 'head'])]
#     visible_text = soup.getText()
#     print(visible_text)


# +
# function to filter tags that are visible on webpage i.e. excluding style, script, meta, etc. tags

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'meta', '[document]']:
        return False
    elif isinstance(element, Comment):                     # check if element is html comment
        return False
    elif re.match(r"[\s\r\n]+",str(element)):              #  to eliminate remaining extra white spaces and new lines
        return False
    else:
        return True


# +
# function to extract only the visible text from the html code of each webpage

def get_text_from_code(page):
    soup = BeautifulSoup(page, "lxml")
    text_in_page = soup.find_all(text=True)                # return all text in page
    visible_text = filter(tag_visible, text_in_page)       # return only visible text
    return " ".join(term.strip() for term in visible_text)


# +
# dict to create inverted index
inverted_index = {}

# dict to store tokens in each web page
webpage_tokens = {}

for file in files:
    web_page = open(pages_folder + file, "r", encoding="utf-8")
    code = web_page.read()
#     print(code)
    text = get_text_from_code(code)                     # get all text actually visible on web page
#     print(text,"\n")
    text = text.lower()
    text = re.sub('[^a-z]+', ' ', text)                 # remove all punctuations and digits
    
    tokens = text.split()
#     print(tokens, "\n")
    
#     # removing stop words from the tokens
#     clean_tokens = [word for word in tokens if word not in stop_words]

#     # stemming the tokens
#     stem_tokens = [st.stem(word) for word in clean_tokens]

#     # checking for stopwords again
#     clean_stem_tokens = [word for word in stem_tokens if word not in stop_words]

#     # converting list of tokens to string
#     clean_stem_tokens = ' '.join(map(str,  clean_stem_tokens))

#     # removing tokens with one or two characters length
#     clean_stem_tokens = shortword.sub('', clean_stem_tokens)
#     print(clean_stem_tokens, "\n")
    
    # removing stop words and stemming each token while only accepting stemmed tokens with length greater than 2 
    clean_stem_tokens = [
        st.stem(token) for token in tokens 
        if (token not in stop_words and st.stem(token) not in stop_words) and len(st.stem(token))>2
    ]
#     print(clean_stem_tokens, "\n")
    
    webpage_tokens[file] = clean_stem_tokens                        # add tokens in web page to dict 
    
    for token in clean_stem_tokens:
        
        freq = inverted_index.setdefault(token,{}).get(file,0)      # get frequency of token and set to 0 if token not in dict
            
        inverted_index.setdefault(token,{})[file] = freq  + 1       # add 1 to frequency of token in current webpage

#         inverted_index.setdefault(token,{})[file] = inverted_index.setdefault(token,{})
#         x = inverted_index.setdefault(token,{})[file]
#         print(x)

# +
# pickling inverted index and tokens

with open(pickle_folder + 'inverted_index.pickle', 'wb') as f:
    pickle.dump(inverted_index,f)
    
with open(pickle_folder + 'webpages_tokens.pickle', 'wb') as f:
    pickle.dump(webpage_tokens,f)
# -

len(inverted_index)
# inverted_index

# +
# for item in webpage_tokens:
# #     print(item)
#     if not webpage_tokens[item]:
#         print(item)
