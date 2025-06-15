# ai_monocler

A Python-based tool to automatically **scrape**, **summarize**, and **analyze** articles using HuggingFace transformers. Summaries include both a short paragraph and key bullet points. 

Emissions tracking is included via [CodeCarbon](https://mlco2.github.io/codecarbon/).

---

## 🚀 Features

- Summarizes long-form text into:
  - ✏️ A concise paragraph
  - ✅ Bullet points of main ideas
- Language support: Russian (via `mbart_ru_sum_gazeta`)
- Tracks carbon emissions with CodeCarbon
- Clean and structured JSON output

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/ai_monocler.git
cd ai_monocler
