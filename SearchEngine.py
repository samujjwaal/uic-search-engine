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
# import urllib.request
import pickle

# +
domain = "uic.edu"
start_url = "https://www.cs.uic.edu/"

# file extensions to ignore while crawling pages
ignore_ext = [
    '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.css', '.js',
    '.aspx', '.png', '.jpg', '.jpeg', '.JPG', '.gif', '.svg', '.ico', '.mp4',
    '.avi', '.tar', '.gz', '.tgz', '.zip'
]

crawl_limit = 3000

# to make sure error log file is initially empty
error_file = "./error_log.txt"
f = open(error_file, "r+")
f.truncate()
f.close()

# queue to perform BFS web traversal
url_q = deque()
url_q.append(start_url)

# list to keep track of traversed URLs
urls_crawled = []
urls_crawled.append(start_url)

# dict to track pages fetched and stored in folder
pages_crawled = {}
page_no = 0

while (len(url_q) != 0):
    
    try:
        url = url_q.popleft()               # fetch the first URL from the queue
        rqst = requests.get(url)            # get html code of web page

        if (rqst.status_code == 200):
            pages_crawled[page_no] = url    

            output_file = "./FetchedPages/" + str(page_no)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)     # create file to store html code

            with open(output_file, "w", encoding="utf-8") as file:
                file.write(rqst.text)
            file.close()

            soup = BeautifulSoup(rqst.text, 'lxml')
            tags_extracted = soup.find_all('a')                 # extract all 'a' tags from page

            for tag in tags_extracted:
                
                l = tag.get('href')

                if l is not None and l.startswith("http"):

                    if not any(ext in l for ext in ignore_ext):

                        if l not in urls_crawled and domain in l:
#                             print(l)
                            url_q.append(l)                 # valid URL to append to the queue
                            urls_crawled.append(l)

            if (len(pages_crawled) > crawl_limit):
                break                                        # stop crawling when reached limit

            page_no += 1

    except Exception as e:
        with open(error_file, "a+") as log:                  # add error message to error log
            log.write(f"Could not connect to {url}")
            log.write(f"\nError occured: {e}\n\n")
        file.close()

        print("Could not connect to ", url)
        print("Error occured: ", e, " \n")
        continue
        
        
with open('pages.pickle', 'wb') as f:
    pickle.dump(pages_crawled,f)

# +
# len(pages_crawled)
# count


# +
# pages_crawled
# -

with open('pages.pickle', 'rb') as f:
    pages = pickle.load(f)

# +
# pages
