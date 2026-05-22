# rag/generator.py

import os
import sys
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.retriever import retrieve_chunks  # type: ignore[import]

MODEL_NAME = "google/flan-t5-small"

print("⏳ Loading flan-t5-base model...")
_tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
_model: T5ForConditionalGeneration = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)  # type: ignore[assignment]
_model.eval()
print("✅ flan-t5-base loaded!\n")


def generate_answer(query: str, top_k: int = 3) -> dict:
    """
    Query se relevant chunks retrieve karo, phir flan-t5-base se answer banao.
    confidence_score FAISS cosine similarity se aata hai — hardcoded nahi.
    """

    # 1) Retrieve
    results = retrieve_chunks(query, top_k=top_k)

    if not results:
        return {
            "answer":           "No relevant information found.",
            "image_path":       None,
            "product_name":     "",
            "source_url":       "",
            "confidence_score": 0.0,
            "chunks_used":      0,
        }

    # 2) Context — title EXCLUDE karo taaki answer mein bracket na aaye
    context_parts: list[str] = []
    for r in results:
        text = r.get("text", "").strip()
        if text:
            context_parts.append(text)

    context = " ".join(context_parts)[:1200]

    # 3) Prompt
    prompt = (
        f"Using only the context below, answer the question with specific "
        f"names, numbers, and locations. Do not repeat the question.\n\n"
        f"Context: {context}\n\n"
        f"Question: {query}\n\n"
        f"Answer:"
    )

    # 4) Tokenize
    inputs = _tokenizer(
        prompt,
        return_tensors="pt",
        max_length=512,
        truncation=True,
    )

    # 5) Generate
    with torch.no_grad():
        outputs = _model.generate(  # type: ignore[operator]
            **inputs,
            max_new_tokens=150,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3,
        )

    answer = _tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # 6) Best chunk metadata
    best = results[0]

    # ✅ Dynamic confidence score from FAISS cosine similarity
    raw_score        = float(best.get("score", 0.0))
    confidence_score = round(min(max(raw_score, 0.0), 1.0), 4)

    return {
        "answer":           answer or "Could not generate an answer.",
        "image_path":       best.get("image_path"),
        "product_name":     best.get("title", best.get("product_name", "TARIL Product")),
        "source_url":       best.get("source", best.get("source_url", "")),
        "confidence_score": confidence_score,
        "chunks_used":      len(results),
    }


if __name__ == "__main__":
    test_queries = [
        "What is the maximum voltage rating of TARIL power transformers?",
        "Which product is used in metal smelting and electrolysis?",
        "Tell me about furnace transformers and cooling options",
        "What transformer is used for renewable energy?",
        "Where are TARIL manufacturing plants?",
    ]

    print("=" * 60)
    print("🧪  GENERATOR TEST")
    print("=" * 60)

    for q in test_queries:
        print(f"\n🔍 Query : {q}")
        result = generate_answer(q)
        print(f"💬 Answer: {result['answer']}")
        print(f"📊 Score : {result['confidence_score']}")
        print(f"📸 Image : {result['image_path']}")
        print("-" * 60)