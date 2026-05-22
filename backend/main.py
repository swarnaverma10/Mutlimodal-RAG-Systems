"""
backend/main.py — TRIL RAG API
Run: py -m uvicorn backend.main:app --port 8000
"""

import os
import sys

# Models will download from HuggingFace on first run

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from rag.generator import generate_answer

app = FastAPI(title="TRIL RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "TRIL RAG API is running ✅"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
def query_rag(data: dict):
    query = data.get("question")
    if not query:
        return JSONResponse(
            status_code=400,
            content={"error": "Request must include a question field."}
        )

    try:
        result = generate_answer(query, top_k=3)

        return {
            "answer":           result.get("answer", ""),
            "confidence_score": result.get("confidence_score", 0.0),  # ✅ sahi key
            "product_name":     result.get("product_name", "TRIL Product"),
            "source_url":       result.get("source_url", ""),
            "image_url":        result.get("image_path", ""),
        }

    except Exception as exc:
        return JSONResponse(
            status_code=500,
            content={
                "error":   "Backend failed to process the query.",
                "details": str(exc),
            }
        )