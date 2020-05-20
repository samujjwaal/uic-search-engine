# Samujjwaal Dey
# Python Script to Preprocess Downloaded webpages


# load dependency libraries
import os
import re
import pickle
from bs4 import BeautifulSoup
from bs4.element import Comment
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


# extracting english stop words
stop_words = stopwords.words("english")

# Initializing Porter Stemmer object
st = PorterStemmer()

# folder to store pickel files
pickle_folder = "./PickleFiles/"
os.makedirs(pickle_folder, exist_ok=True)

# folder name storing downloaded web pages
pages_folder = "./FetchedPages/"
filenames = os.listdir(pages_folder)

# list to store filenames of all stored crawled webpages
files = []

for name in filenames:
    files.append(name)


# function to filter tags that are visible on webpage i.e. excluding style, script, meta, etc. tags


def tag_visible(element):
    if element.parent.name in ["style", "script", "head", "meta", "[document]"]:
        return False
    # check if element is html comment
    elif isinstance(element, Comment):
        return False
    #  to eliminate remaining extra white spaces and new lines
    elif re.match(r"[\s\r\n]+", str(element)):
        return False
    else:
        return True


# function to extract only the visible text from the html code of each webpage


def get_text_from_code(page):
    soup = BeautifulSoup(page, "lxml")
    # return all text in page
    text_in_page = soup.find_all(text=True)
    # return only visible text
    visible_text = filter(tag_visible, text_in_page)
    return " ".join(term.strip() for term in visible_text)


# dict to create inverted index
inverted_index = {}

# dict to store tokens in each web page
webpage_tokens = {}

for file in files:
    web_page = open(pages_folder + file, "r", encoding="utf-8")
    code = web_page.read()
    # get all text actually visible on web page
    text = get_text_from_code(code)
    text = text.lower()
    # remove all punctuations and digits
    text = re.sub("[^a-z]+", " ", text)
    tokens = text.split()
    # removing stop words and stemming each token while only accepting stemmed tokens with length greater than 2
    clean_stem_tokens = [
        st.stem(token)
        for token in tokens
        if (token not in stop_words and st.stem(token) not in stop_words)
        and len(st.stem(token)) > 2
    ]

    # add tokens in web page to dict
    webpage_tokens[file] = clean_stem_tokens

    for token in clean_stem_tokens:
        # get frequency of token and set to 0 if token not in dict
        freq = inverted_index.setdefault(token, {}).get(file, 0)

        # add 1 to frequency of token in current webpage
        inverted_index.setdefault(token, {})[file] = freq + 1


# pickling inverted index and web page tokens
with open(pickle_folder + "6000_inverted_index.pickle", "wb") as f:
    pickle.dump(inverted_index, f)

with open(pickle_folder + "6000_webpages_tokens.pickle", "wb") as f:
    pickle.dump(webpage_tokens, f)
