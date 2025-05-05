import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
import os

def scrape_page(url):
    try:
        print(f"Scraping: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        content = []

        if soup.title:
            content.append(soup.title.get_text(strip=True))

        for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
            text = tag.get_text(strip=True)
            if text:
                content.append(text)

        return '\n'.join(content), soup
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return "", None

def extract_links(soup, base_url):
    links = set()
    skip_ext = ('.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx')
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == urlparse(base_url).netloc and not full_url.lower().endswith(skip_ext):
            links.add(full_url)
    return links

def save_checkpoint(visited, to_visit):
    with open("data/checkpoint.json", "w") as cp:
        json.dump({"visited": list(visited), "to_visit": list(to_visit)}, cp)

def load_checkpoint():
    if os.path.exists("data/checkpoint.json"):
        with open("data/checkpoint.json") as cp:
            data = json.load(cp)
            return set(data["visited"]), set(data["to_visit"])
    return set(), set(["https://www.rawmilkinstitute.org"])

if __name__ == "__main__":
    visited, to_visit = load_checkpoint()

    with open("data/example_output.txt", "a") as f:
        while to_visit:
            url = to_visit.pop()
            if url in visited:
                continue
            visited.add(url)
            print(f"Visiting ({len(visited)}): {url}")
            time.sleep(5)

            content, soup = scrape_page(url)
            if content:
                f.write(f"URL: {url}\n{content}\n\n")

            if soup:
                new_links = extract_links(soup, url)
                print(f"  Found {len(new_links)} new links")
                to_visit.update(new_links - visited)

            if len(visited) % 10 == 0:
                save_checkpoint(visited, to_visit)