import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from whoosh.fields import Schema, TEXT, ID
from whoosh import index
import os
import urllib.parse

class Crawler:
    def __init__(self, start_url):
        self.running = True
        self.xx = 200
        self.start_url = start_url
        self.agenda = [start_url]  # Start with one URL
        self.visites = set()  # A set to store visited URLs to avoid duplicates
        self.visites.add(self.start_url)

        # Parse the starting URL to get the base domain
        parsed_url = urllib.parse.urlparse(start_url)
        self.base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

        print("Base domain:", self.base_domain)

        #creating a Schema
        self.schema = Schema(url = ID(stored=True),
                title = TEXT(stored=True),
                headder = TEXT(stored=True),
                content = TEXT(stored=True))
        #create indexdir
        if not os.path.exists("indexdir"):
            os.mkdir("indexdir")
        self.ix = index.create_in("indexdir", self.schema)

    def get_all_links(self,itteration): 

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
                        if not full_url.startswith(self.base_domain):
                            print("External URL:", full_url)
                            continue

                        # Add the link to the agenda if it hasn't been visited
                        if full_url not in self.visites:
                            self.visites.add(full_url)  # Mark the current URL as visited
                            print(len(self.visites))
                            self.agenda.append(full_url)
                            print("Added to agenda:", full_url)
                            if len(self.visites) > itteration:
                                self.agenda.clear()
                                break

            except Exception as e:
                print("Error fetching URL:", e)

        return self.visites
    
    def extract_info(self, all_links):
        writer = self.ix.writer()
        for url in all_links:
            try:
                r = requests.get(url)
                soup = BeautifulSoup(r.content, 'html.parser')

                # Get title
                title_html = soup.find('title')
                title = title_html.get_text(strip=True) if title_html else ''

                # Get header text
                h1_html = soup.find('h1')
                h1 = h1_html.get_text(strip=True) if h1_html else ''

                # Get content: concatenate text from <p> and <pre> tags
                p_text = ''
                pre_text = ''

                # Extract <p> text
                p_tags = soup.find_all('p')  # Finds all <p> tags
                if p_tags:
                    p_text = ' '.join(tag.get_text(strip=True) for tag in p_tags)

                # Extract <pre> text
                pre_tags = soup.find_all('pre')  # Finds all <pre> tags
                if pre_tags:
                    pre_text = ' '.join(tag.get_text(strip=True) for tag in pre_tags)

                # Combine <p> and <pre> text
                combined_content = f"{p_text} {pre_text}".strip()

                # Add document to Whoosh index
                writer.add_document(url=url, title=title, headder=h1, content=combined_content)

                print(f"url: {url}, title: {title}, header: {h1}, content: {combined_content}")

            except Exception as e:
                print(f"Error processing {url}: {e}")

        writer.commit()
        


