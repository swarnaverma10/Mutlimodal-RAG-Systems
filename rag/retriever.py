# rag/retriever.py

import faiss
import json
import numpy as np
import os
from sentence_transformers import SentenceTransformer

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH  = os.path.join(BASE_DIR, "data", "vector_store", "faiss_index")
META_PATH   = os.path.join(BASE_DIR, "data", "vector_store", "metadata.json")

# ── Load model + index (module-level, ek baar load hoga) ─────────────────────
print("⏳ Loading embedding model...")
_embed_model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ Embedding model loaded!")

print("⏳ Loading FAISS index...")
_index = faiss.read_index(INDEX_PATH)
print(f"✅ FAISS index loaded — {_index.ntotal} vectors")

with open(META_PATH, "r", encoding="utf-8") as f:
    _metadata: list[dict] = json.load(f)
print(f"✅ Metadata loaded — {len(_metadata)} chunks\n")


# ── Main function ─────────────────────────────────────────────────────────────
def retrieve_chunks(query: str, top_k: int = 3) -> list[dict]:
    """
    Query string se top-k relevant chunks retrieve karo FAISS se.

    Args:
        query:  User ka sawaal
        top_k:  Kitne chunks chahiye (default 3)

    Returns:
        List of dicts with keys: text, image_path, source, title, score
    """
    # 1) Query embed karo
    query_vec = _embed_model.encode([query], normalize_embeddings=True)
    query_vec = np.array(query_vec, dtype="float32")

    # 2) FAISS search
    k         = min(top_k, _index.ntotal)
    distances, indices = _index.search(query_vec, k)

    # 3) Results assemble karo
    results: list[dict] = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < 0 or idx >= len(_metadata):
            continue
        chunk = dict(_metadata[idx])          # copy
        chunk["score"] = float(dist)          # cosine similarity (normalized)
        results.append(chunk)

    return results


# ── Standalone test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_queries = [
        "What projects does TRIL offer?",
        "TRIL residential apartments features",
        "price of TRIL flats",
    ]

    print("=" * 60)
    print("🧪  RETRIEVER TEST")
    print("=" * 60)

    for q in test_queries:
        print(f"\n🔍 Query: {q}")
        chunks = retrieve_chunks(q, top_k=3)
        for i, c in enumerate(chunks, 1):
            print(f"  [{i}] Score: {c['score']:.4f} | Title: {c.get('title','—')}")
            print(f"       Text : {c.get('text','')[:100]}...")
        print("-" * 60)