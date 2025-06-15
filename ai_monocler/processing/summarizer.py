import json
import os
from pathlib import Path
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent / "data" / "articles.json"
OUTPUT_PATH = BASE_DIR.parent / "data" / "summaries.json"

MODEL_NAME = "IlyaGusev/mbart_ru_sum_gazeta"

print("Loading tokenizer and model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
summarizer = pipeline("text2text-generation", model=model, tokenizer=tokenizer, device=-1)

MAX_INPUT_LENGTH = 1024


def safe_summarize(text):
    text = text.strip()
    if len(text) > 3500:
        text = text[:3500]

    # Prompt for paragraph
    paragraph_prompt = f"Сделай краткое резюме статьи:\n{text}"
    paragraph = summarizer(paragraph_prompt, max_length=180, min_length=40, do_sample=False)[0]["generated_text"]

    # Prompt for bullet points
    bullets_prompt = f"Выдели основные мысли статьи в виде списка:\n{text}"
    bullets = summarizer(bullets_prompt, max_length=200, min_length=50, do_sample=False)[0]["generated_text"]

    return paragraph, bullets


def main():
    tracker = EmissionsTracker(project_name="ai_monocler")
    tracker.start()

    if not os.path.exists(DATA_PATH):
        print(f"ERROR: Input file not found: {DATA_PATH}")
        tracker.stop()
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
            summary_text, bullet_points = safe_summarize(content)
            summaries.append({
                "url": article.get("url"),
                "title": title,
                "summary": summary_text,
                "bullet_points": bullet_points
            })
            print(f"[{i}/{total}] Summarized: {title}")
        except Exception as e:
            print(f"❌ Failed to summarize '{title}': {e}")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)

    print(f"Summaries saved to {OUTPUT_PATH}")

    emissions = tracker.stop()
    print(f"Summaries saved to {OUTPUT_PATH}")
    print(f"Carbon emissions: {emissions:.6f} kg CO₂")


if __name__ == "__main__":
    main()
