import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

start_url = "https://vm009.rz.uos.de/crawl/index.html"
agenda = [start_url]  # Start with one URL
visited = set()  # A set to store visited URLs to avoid duplicates

while agenda:
    # Get the next URL to process
    current_url = agenda.pop()  # Removes the last URL from the list
    if current_url in visited:  # Skip URLs that were already visited
        continue

    print("Url", current_url)
    visited.add(current_url)  # Mark the current URL as visited

    try:
        r = requests.get(current_url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')

            # Find all links on the current page
            all_links = soup.find_all('a')

            for link in all_links:
                href = link.get('href')  # Extract the href attribute from the <a> tag
                if not href:
                    continue  # Skip if href is empty or None
                
                # Join the href with the base URL
                full_url = urljoin(current_url, href)

                # Only process internal URLs
                if not full_url.startswith("https://vm009.rz.uos.de/"):
                    print("URL is external.")
                    continue

                # Add the link to the agenda if it hasn't been visited
                if full_url not in visited:
                    agenda.append(full_url)
                    print("Added to agenda:", full_url)

    except Exception as e:
        print("Error fetching URL:", e)#


