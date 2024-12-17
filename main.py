import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from crawler import Crawler
#from searchengine import SearchEngine


start_url = "https://vm009.rz.uos.de/crawl/index.html"

crwl = Crawler(start_url)
all_links = crwl.get_all_links()
print("all links:", all_links)
crwl.extract_info(all_links)






