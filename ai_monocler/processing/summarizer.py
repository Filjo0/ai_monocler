import json
import os
from pathlib import Path

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

BASE_DIR = Path(__file__).resolve().parent  # this is the 'processing' folder
DATA_PATH = BASE_DIR.parent / "data" / "articles.json"
OUTPUT_PATH = BASE_DIR.parent / "data" / "summaries.json"

# Use the Russian-optimized summarization model
MODEL_NAME = "csebuetnlp/mT5_multilingual_XLSum"

print("Loading summarization pipeline...")

# Disable fast tokenizer due to SentencePiece compatibility
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer, device=-1)

MAX_INPUT_LENGTH = 1024  # max tokens - tokenizer will truncate accordingly


def safe_summarize(text):
    # Hugging Face pipeline truncates automatically, but we can trim by chars to be safe
    max_chars = 3500
    text = text.strip()
    if len(text) > max_chars:
        text = text[:max_chars]
    return summarizer(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']


def main():
    if not os.path.exists(DATA_PATH):
        print(f"ERROR: Input file not found: {DATA_PATH}")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    summaries = []
    total = len(articles)
    print(f"Loaded {total} articles.")

    for i, article in enumerate(articles, 1):
        title = article.get("title", "No Title")
        content = article.get("content", "").strip()
        if not content or len(content) < 100:
            print(f"Skipping article {i}/{total}: '{title}' (content too short)")
            continue

        try:
            summary = safe_summarize(content)
            summaries.append({
                "url": article.get("url"),
                "title": title,
                "summary": summary
            })
            print(f"[{i}/{total}] Summarized: {title}")
        except Exception as e:
            print(f"Failed to summarize '{title}': {e}")

    # Save summaries
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)

    print(f"Summaries saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
