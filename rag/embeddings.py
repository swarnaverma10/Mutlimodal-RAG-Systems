"""
rag/embeddings.py
-----------------
HuggingFace embeddings (FREE) + FAISS index
"""

import os
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_DATASETS_OFFLINE"] = "1" 
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# ── Config ────────────────────────────────────────────────────────────────────
CHUNKS_PATH   = "data/processed/chunks.json"
VECTOR_STORE  = "data/vector_store"
INDEX_PATH    = f"{VECTOR_STORE}/faiss_index"
METADATA_PATH = f"{VECTOR_STORE}/metadata.json"

MODEL_NAME = "all-MiniLM-L6-v2"
EMBED_DIM  = 384

# ── Load model ────────────────────────────────────────────────────────────────
print("📦 Loading embedding model...")
model = SentenceTransformer(MODEL_NAME)
print("✅ Model loaded.\n")


def load_chunks(path: str) -> list[dict]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ chunks.json not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_embeddings(texts: list[str]) -> np.ndarray:
    vectors = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    faiss.normalize_L2(vectors)
    return vectors.astype("float32")


def build_and_save_index(vectors: np.ndarray):
    index = faiss.IndexFlatIP(EMBED_DIM)
    index.add(vectors)
    os.makedirs(VECTOR_STORE, exist_ok=True)
    faiss.write_index(index, INDEX_PATH)
    print(f"✅ FAISS index saved: {INDEX_PATH}")
    print(f"   Total vectors: {index.ntotal}")


def save_metadata(chunks: list[dict]):
    metadata = []
    for i, chunk in enumerate(chunks):
        metadata.append({
            "faiss_id":     i,
            "chunk_id":     f"chunk_{i:04d}",
            "product_name": chunk.get("title", "Unknown"),
            "category":     chunk.get("title", "General"),
            "image_path":   chunk.get("image_path", ""),
            "source_url":   chunk.get("source", ""),
            "text":         chunk.get("text", ""),
        })
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"✅ Metadata saved: {METADATA_PATH}")


def main():
    print("=" * 55)
    print("  TRIL RAG — Embedding Pipeline (HuggingFace FREE)")
    print("=" * 55)

    print(f"\n📂 Loading chunks: {CHUNKS_PATH}")
    chunks = load_chunks(CHUNKS_PATH)
    print(f"   Found {len(chunks)} chunks.\n")

    texts = [chunk.get("text", "") for chunk in chunks]
    print("🔢 Generating embeddings locally...")
    vectors = generate_embeddings(texts)
    print(f"   Shape: {vectors.shape}\n")

    print("🔨 Building FAISS index...")
    build_and_save_index(vectors)

    print("\n💾 Saving metadata...")
    save_metadata(chunks)

    print(f"\n{'=' * 55}")
    print(f"✅ Done! Ready for next step.")
    print(f"   Next: py rag/retriever.py")
    print("=" * 55)


if __name__ == "__main__":
    main()