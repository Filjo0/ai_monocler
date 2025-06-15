import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict


def scrape_article(url: str) -> Optional[Dict[str, str]]:
    """
    Extracts title and cleaned article content from a monocler.ru article page.
    Filters out meta-paragraphs and centered promotional content.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        header = soup.find("h1", class_="post-heading")
        title = header.text.strip() if header else "No title"

        # Extract main article content
        content_div = soup.find("article", class_="entry-content")
        if not content_div:
            print(f"No content found for {url}")
            return None

        paragraphs = []
        for p in content_div.find_all("p"):
            # Skip ads and meta elements
            if "post-meta" in p.get("class", []):
                continue
            if p.get("style") == "text-align: center;":
                continue
            text = p.get_text(strip=True)
            if text:
                paragraphs.append(text)

        full_text = "\n\n".join(paragraphs)

        return {
            "url": url,
            "title": title,
            "content": full_text
        }

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None
