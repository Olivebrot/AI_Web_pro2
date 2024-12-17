import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from whoosh import index
import os

class Crawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.agenda = [start_url]  # Start with one URL
        self.visites = set()  # A set to store visited URLs to avoid duplicates
        self.visites.add(self.start_url)

        # Define schema for Whoosh indexing, should be done in __init__ method
        self.schema = Schema(url=ID(stored=True), content=TEXT(stored=True))
    
    def get_all_links(self): 

        while self.agenda:
            current_url = self.agenda.pop()  # Removes the last URL from the list

            print("Processing URL:", current_url)
            

            try:
                r = requests.get(current_url)
                if r.status_code == 200:
                    
                    soup = BeautifulSoup(r.content, 'html.parser')

                    # Find all links on the current page
                    page_links = soup.find_all('a')

                    for link in page_links:
                        href = link.get('href')  # Extract the href attribute from the <a> tag
                        if not href:
                            continue  # Skip if href is empty or None
                        
                        # Join the href with the base URL
                        full_url = urljoin(current_url, href)

                        # Only process internal URLs
                        if not full_url.startswith("https://vm009.rz.uos.de/"):
                            print("External URL:", full_url)
                            continue

                        # Add the link to the agenda if it hasn't been visited
                        if full_url not in self.visites:
                            self.visites.add(full_url)  # Mark the current URL as visited
                            self.agenda.append(full_url)
                            print("Added to agenda:", full_url)

            except Exception as e:
                print("Error fetching URL:", e)

        return self.visites
    
    def extract_info(self, all_links):
        # Create an index directory where the Whoosh index will be stored
        index_dir = "indexdir" 
        
        # Create the directory for Whoosh index if it doesn't exist
        if not os.path.exists(index_dir):
            os.mkdir(index_dir)
        
        # Create an index if it doesn't exist
        if not os.path.exists(os.path.join(index_dir, "segments")):
            self.index = create_in(index_dir, self.schema)
        else:
            self.index = index.open_dir(index_dir)

        # Open the index writer to add documents
        writer = self.index.writer()

        for url in all_links:
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.content, 'html.parser')
                    content = soup.get_text()  # Extract all text from the page

                    # Add the document to the index with the URL and content
                    writer.add_document(url=url, content=content)
                    print(f"Indexed URL: {url}")
            except Exception as e:
                print(f"Error indexing {url}: {e}")

        # Commit the changes to the index
        writer.commit()

        print("Indexing complete!")


