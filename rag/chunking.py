import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAW_PATH = BASE_DIR.parent / "data" / "raw" / "products.json"
PROCESSED_PATH = BASE_DIR.parent / "data" / "processed" / "chunks.json"

with open(RAW_PATH, "r", encoding="utf-8") as f:
    products = json.load(f)

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


def split_text(text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - chunk_overlap)
    return chunks

chunks = []

for item in products:
    split_texts = split_text(item["content"])

    for chunk in split_texts:

        chunks.append({
            "text": chunk,
            "image_path": item["image_path"],
            "source": item["source"],
            "title": item["title"]
        })

PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(PROCESSED_PATH, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=4)

print("Chunking Done")