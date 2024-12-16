import requests
from bs4 import BeautifulSoup

prefix = 'https://vm009.rz.uos.de/crawl/index.html'

start_url = prefix

agenda = [start_url]

while agenda:
    url = agenda.pop()
    print("Get ",url)
    r = requests.get(url)
    print(r, r.encoding)
    if r.status_code == 200:
        print(r.headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.find_all('a'))
        