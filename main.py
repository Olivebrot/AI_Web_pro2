import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from crawler import Crawler
#from searchengine import SearchEngine


base_url = "https://vm009.rz.uos.de/crawl/index.html"
crawler = Crawler(base_url)

crawler.crawl(base_url,4)
index = open_dir("index")

print(index)



