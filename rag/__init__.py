# rag/__init__.py
# Pylance warning fix — lazy imports, no direct symbol re-export

def retrieve_chunks(query: str, top_k: int = 3) -> list[dict]:
    from rag.retriever import retrieve_chunks as _fn   # type: ignore[import]
    return _fn(query, top_k)

def generate_answer(query: str, top_k: int = 3) -> dict:
    from rag.generator import generate_answer as _fn   # type: ignore[import]
    return _fn(query, top_k)

__all__ = ["retrieve_chunks", "generate_answer"]