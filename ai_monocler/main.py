import json
import os

from tqdm import tqdm

from ai_monocler.scraping.article_scraper import scrape_article
from ai_monocler.scraping.list_scraper import get_all_article_links

base_url = "https://monocler.ru"
category = "category/psychology"

if __name__ == "__main__":
    print("Fetching article links...")
    urls = get_all_article_links(base_url, category)
    print(f"Found {len(urls)} articles.\n")

    articles = []

    for url in tqdm(urls):
        article = scrape_article(url)
        if article:
            articles.append(article)

    print(f"\nSaving {len(articles)} articles to data/articles.json")

    os.makedirs("ai_monocler/data", exist_ok=True)

    with open("data/articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
