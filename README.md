# Web Search Engine on UIC Domain
![GitHub](https://img.shields.io/github/license/samujjwaal/UIC-search-engine)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/samujjwaal/UIC-search-engine/master)
![GitHub top language](https://img.shields.io/github/languages/top/samujjwaal/UIC-search-engine)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![GitHub repo size](https://img.shields.io/github/repo-size/samujjwaal/UIC-search-engine)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/samujjwaal/UIC-search-engine)

Web search engine to retrieve most relevant web-pages for user search query from web-pages crawled on the UIC domain

This project was done as the term project for CS582: Information Retrieval course at the University of Illinois at Chicago during the Spring 2020 term.

The goal of the project is to design and implement a web search engine for the [UIC domain](https://www.uic.edu/). The search engine includes a web crawler, preprocessing and indexing of web pages, and an IR system implementing a vector-space model to retrieve webpages relevant to an input user query.

A broad description of functionalities to be included in the web search engine can be found [here](ProjectTasks.pdf). 

## Software Description

The software is designed in Python3.8, and all functions are modularized so that they can be extended further for use in other projects and future work. 

The search engine crawls, collects, and preprocesses 6000 webpages from the [UIC domain](https://www.uic.edu/), which takes around 3 hours to complete. 

So to execute the code without first crawling the UIC domain, all the pickle files needed to execute the code are included inside the [PickleFiles](PickleFiles) folder. 

The [search_query.py](search_query.py) script file can be executed from the terminal to execute the search engine right away. However, the python scripts to execute the [crawling](uic_crawler.py) of web-pages and their [preprocessing](preprocessor.py) are also provided in the repository.

Detailed description of the various components and functionalities of the search engine can be found in the accompanying [project report](ProjectReport.pdf).

The various alternate trial-error code snippets executed during developing the search engine are in the form of [Jupyter Notebooks](JupyterNBs). 

## Usage Details

To execute the web search engine, run the following command in the terminal:

`python search_query.py`

Similarly the python scripts to execute the [crawling](uic_crawler.py) of web-pages and their [preprocessing](preprocessor.py) can also be executed from the terminal.
