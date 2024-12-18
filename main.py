import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from crawler import Crawler
from search import Search


start_url = "https://vm009.rz.uos.de/crawl/index.html"

crwl = Crawler(start_url)
all_links = crwl.get_all_links()
print("done")
# x = len(all_links)
# for links in all_links:
#     print("link",x,":",links)
#     x = x-1
# print(all_links)
crwl.extract_info(all_links)

# Create a Search object
srch = Search(field_weights={"title": 2.0, "headder": 1.5, "content": 1.0})

# User's search query
user_query = input("Enter your search query: ")

# Perform search and print results
results = srch.search_all_fields(user_query)
if results:
    print("\nSearch Results:\n")
    for idx, result in enumerate(results, start=1):
        print(f"Result {idx}")
        print(f"URL: {result['url']}")
        print(f"Title: {result['title']}")
        print(f"Header: {result['headder']}")
        print(f"Snippet: {result['content_snippet']}")
        print(f"Score: {result['score']}")
        print("-" * 50)
else:
    print("No results found!")





#crwl.test_ix()






