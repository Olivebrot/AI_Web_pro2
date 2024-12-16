import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import os
from flask import Flask, request, jsonify

class Crawler:
    def __init__(self, base_url, index_dir="index"):
        self.base_url = base_url
        self.visited = set()
        self.index_dir = index_dir

        # Define schema for indexing
        self.schema = Schema(
            url=ID(stored=True, unique=True),
            title=TEXT(stored=True),
            content=TEXT
        )

        # Create index directory if it doesn't exist
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)

        # Create or open index
        self.index = create_in(self.index_dir, self.schema)

    def fetch_page(self, url):
        """Fetch page content from a URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_links(self, url, html):
        """Extract and return all valid links from the page."""
        soup = BeautifulSoup(html, "html.parser")
        links = set()
        for tag in soup.find_all("a", href=True):
            href = tag['href']
            if href.startswith("http"):
                links.add(href)
            elif href.startswith("/"):
                links.add(self.base_url + href)
        return links

    def extract_content(self, html):
        """Extract the title and main content from the HTML."""
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string if soup.title else ""
        text = soup.get_text(separator=" ", strip=True)
        return title, text

    def index_page(self, url, title, content):
        """Index a page's content."""
        writer = self.index.writer()
        writer.add_document(url=url, title=title, content=content)
        writer.commit()

    def crawl(self, url, depth=1):
        """Crawl a URL up to a certain depth."""
        if depth == 0 or url in self.visited:
            return

        print(f"Crawling: {url}")
        self.visited.add(url)

        html = self.fetch_page(url)
        if not html:
            return

        title, content = self.extract_content(html)
        self.index_page(url, title, content)

        links = self.parse_links(url, html)
        for link in links:
            self.crawl(link, depth - 1)

