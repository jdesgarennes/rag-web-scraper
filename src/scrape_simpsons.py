import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.simpsonsarchive.com"
INDEX_URL = f"{BASE_URL}/episodes/"

def get_episode_links():
    res = requests.get(INDEX_URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.find_all('a', href=True)
    txt_links = [BASE_URL + link['href'] for link in links if link['href'].endswith('.txt')]
    return txt_links

def fetch_and_save_all(output_file="simpsons_scripts.txt"):
    links = get_episode_links()
    print(f"Found {len(links)} scripts.")
    
    with open(output_file, 'w') as out:
        for i, url in enumerate(links):
            try:
                res = requests.get(url)
                out.write(f"\n\n--- {url} ---\n\n")
                out.write(res.text)
                print(f"[{i+1}/{len(links)}] Fetched: {url}")
                time.sleep(0.5)  # polite delay
            except Exception as e:
                print(f"Failed to fetch {url}: {e}")

if __name__ == "__main__":
    fetch_and_save_all()
