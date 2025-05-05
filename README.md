# Web Scraper for RAG Data Collection

This tool is a simple and flexible web scraper designed to collect, clean, and chunk web content for use in RAG (Retrieval-Augmented Generation) systems.

## 🚀 Features

- Scrape any public webpage (HTML or `.txt`)
- Extracts and cleans main content (paragraphs, dialogue, etc.)
- Splits text into manageable chunks for embedding
- Supports piping into any vector DB like Chroma or FAISS

## 📁 Files

- `scrape_and_chunk.py` — CLI tool to scrape a URL and chunk the result
- `chunker.py` — Utility to split raw text into overlapping token-aware chunks

## ▶️ Usage

### Scrape a single URL

```bash
python scrape_and_chunk.py https://example.com/article
