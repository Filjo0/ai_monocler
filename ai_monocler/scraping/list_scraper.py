import requests
from bs4 import BeautifulSoup
from typing import List, Any


def get_article_links(listing_url: str) -> tuple[list[Any], BeautifulSoup]:
    """
    Extract article URLs from pages with <div class="et-description"> blocks.
    """
    response = requests.get(listing_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    articles = soup.find_all('div', class_='et-description')
    for article in articles:
        h2 = article.find('h2')
        a_tag = h2.find('a') if h2 else None
        if a_tag and 'href' in a_tag.attrs:
            links.append(a_tag['href'])

    return links, soup


def get_all_article_links(base_url: str, category: str) -> List[str]:
    """
    Iterates through paginated listing pages until there are no more "← Раньше" links.
    """
    base_url = base_url.rstrip('/')
    category = category.strip('/')
    page = 1
    all_links = []

    while True:
        if page == 1:
            url = f"{base_url}/{category}"
        else:
            url = f"{base_url}/{category}/page/{page}/"

        print(f"Scraping: {url}")
        try:
            links, soup = get_article_links(url)
            all_links.extend(links)
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            break

        # Check if "← previous" pagination exists. If not - stop.
        pagination = soup.find('div', class_='pagination')
        if not pagination or not pagination.find('div', class_='alignleft'):
            print("No more pages found.")
            break

        page += 1

    return list(set(all_links))  # Deduplicate
