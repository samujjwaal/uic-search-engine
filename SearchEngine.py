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

# # Crawler

# load dependency libraries
import requests
from bs4 import BeautifulSoup
from collections import deque
import os
import urllib.request
import pickle

q = deque()
url = "https://www.cs.uic.edu/"
q.append(url)
q

domain = "uic.edu"
urls_crawled = []
urls_crawled.append(domain)

rqst = requests.get(url)


# +
# rqst.text
# -

soup = BeautifulSoup(rqst.text,'lxml')

# +
tags = soup.find_all('a')

for tag in tags:
    l = tag.get('href')
    if l is not None and l .startswith("http") and domain in l:
        print(l)
