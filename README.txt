SRCH    Ai and the Web winter semester 2024/2025

A simple search engine made with whoosh, beautifulsoup and falsk

crawler.py is crawling with beautifulsoup the website and saving Headder, Title, Text, URL using whoosh

search.py is using the whoosh index to search

app.py connects everything. It makes a website using falsk.

index.html is the start website where the user can input url and text he wants to search.

results.html displays the searched result after the website has been crawled and searched using crawler.py and search.py