# Samujjwaal Dey
# Python Script to perform web crawling on the UIC domain


# load dependency libraries
import requests
import os
import pickle
from bs4 import BeautifulSoup
from collections import deque

# domain for the crawler
domain = "uic.edu"

# starting URL for the crawler BFS algorithm
start_url = "https://cs.uic.edu"

# folder name to store downloaded web pages
pages_folder = "./FetchedPages/"

# file extensions to ignore while crawling pages
ignore_ext = [
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".css",
    ".js",
    ".aspx",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".mp4",
    ".avi",
    ".tar",
    ".gz",
    ".tgz",
    ".zip",
]

# number of pages to crawl before stopping
crawl_limit = 6000

# to make sure error log file is initially empty
error_file = "error_log.txt"
f = open(error_file, "w+")
# f.truncate()
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

while url_q:

    try:
        url = url_q.popleft()  # fetch the first URL from the queue
        rqst = requests.get(url)  # get html code of web page

        if rqst.status_code == 200:

            soup = BeautifulSoup(rqst.text, "lxml")
            tags_extracted = soup.find_all("a")  # extract all 'a' tags from page

            if (
                len(tags_extracted) != 0
            ):  # to reject pages which don't link to another page

                pages_crawled[page_no] = url

                output_file = pages_folder + str(page_no)

                os.makedirs(
                    os.path.dirname(output_file), exist_ok=True
                )  # create file to store html code

                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(
                        rqst.text
                    )  # storing downloaded content of webpage to file
                file.close()

                for tag in tags_extracted:

                    link = tag.get("href")

                    if (
                        link is not None
                        and link.startswith("http")
                        and not any(ext in link.lower() for ext in ignore_ext)
                    ):

                        link = link.lower()
                        link = link.split("#")[
                            0
                        ]  # removing intra page anchor tags from URL
                        link = link.split("?", maxsplit=1)[
                            0
                        ]  # removing query parameters from URL
                        link = link.rstrip("/")  # removing trailing / from URL
                        link = link.strip()

                        if link not in urls_crawled and domain in link:
                            url_q.append(link)  # valid URL to append to the queue
                            urls_crawled.append(link)

                if len(pages_crawled) > crawl_limit:
                    break  # stop crawling when reached limit

                page_no += 1

    except Exception as e:
        with open(error_file, "a+") as log:  # add error message to error log
            log.write(f"Could not connect to {url}")
            log.write(f"\nError occured: {e}\n\n")
        file.close()

        print("Could not connect to ", url)
        print("Error occured: ", e, " \n")
        continue


# Creating folder to store pickle files
pickle_folder = "./PickleFiles/"
os.makedirs(pickle_folder, exist_ok=True)

# Pickling the dict of crawled pages
with open(pickle_folder + "6000_pages_crawled.pickle", "wb") as f:
    pickle.dump(pages_crawled, f)
