import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time


def fetch_page(url, timeout=10):
    """Fetch a single page and return its text content."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=timeout, verify=False)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        text = soup.get_text(separator=" ", strip=True)
        text = " ".join(text.split())

        return text
    except Exception as e:
        return None


def fetch_all_pages(base_url, max_pages=50, delay=1):
    """Fetch all pages from a website starting from base_url."""
    visited = set()
    to_visit = [base_url]
    pages_content = {}

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)

        if url in visited:
            continue

        visited.add(url)

        text = fetch_page(url)
        if text and len(text) > 100:
            pages_content[url] = text

        time.sleep(delay)

        if len(pages_content) >= max_pages:
            break

        if len(visited) < max_pages:
            try:
                response = requests.get(url, timeout=5, verify=False)
                soup = BeautifulSoup(response.content, "html.parser")

                for link in soup.find_all("a", href=True):
                    full_url = urljoin(url, link["href"])
                    parsed = urlparse(full_url)

                    if parsed.netloc == urlparse(base_url).netloc:
                        if full_url not in visited:
                            to_visit.append(full_url)
            except:
                pass

    return pages_content


if __name__ == "__main__":
    test_url = "https://example.com"
    print(f"Testing fetch on: {test_url}")
    pages = fetch_all_pages(test_url, max_pages=2)
    print(f"Fetched {len(pages)} pages")
    for url, content in pages.items():
        print(f"{url}: {content[:100]}...")
