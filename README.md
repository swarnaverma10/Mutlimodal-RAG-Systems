# TARIL Multimodal RAG System
**Candidate:** Swarna Verma  
**Data Source:** [transformerindia.com](https://www.transformerindia.com)  
**Task:** Internship Interview Assignment

---

## Overview

A Retrieval-Augmented Generation (RAG) system that answers natural language questions about TARIL (Transformers & Rectifiers India Ltd.) — India's largest transformer manufacturer — using real data scraped from their website. Every answer is accompanied by a relevant product image retrieved from the knowledge base.

---

## System Architecture

```
User Question (Streamlit UI)
        ↓
FastAPI /query endpoint
        ↓
FAISS Vector Search → Top-3 Relevant Chunks
        ↓
flan-t5-base LLM → Grounded Answer
        ↓
Response: Answer + Product Image + Confidence Score
        ↓
Streamlit Display
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Scraping | BeautifulSoup + Requests |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` (FREE, local) |
| Vector Store | FAISS `IndexFlatIP` (cosine similarity) |
| LLM | Google `flan-t5-base` (FREE, local) |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |

---

## Project Structure

```
multimodal-rag-system/
│
├── data/
│   ├── raw/                    # Scraped HTML/JSON data
│   ├── processed/
│   │   └── chunks.json         # 26 chunks (text + image_path + metadata)
│   └── vector_store/
│       ├── faiss_index         # FAISS index (26 vectors, 384-dim)
│       └── metadata.json       # Chunk metadata linked to vectors
│
├── images/                     # Downloaded product images
│
├── rag/
│   ├── embeddings.py           # HuggingFace embedding generation
│   ├── retriever.py            # FAISS search → top-k chunks
│   ├── generator.py            # flan-t5-base answer generation
│   └── __init__.py
│
├── backend/
│   ├── main.py                 # FastAPI server (POST /query)
│   └── __init__.py
│
├── frontend/
│   └── app.py                  # Streamlit UI
│
├── .env
├── requirements.txt
└── README.md
```

---

## Setup & Run

### 1. Clone & Setup
```bash
git clone <repo>
cd multimodal-rag-system
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Start Backend
```bash
py -m uvicorn backend.main:app --port 8000
```
Verify: `http://localhost:8000/health` → `{"status": "ok"}`

### 3. Start Frontend (new terminal)
```bash
py -m streamlit run frontend/app.py
```
Open: `http://localhost:8501`

---

## API Reference

### `POST /query`

**Request:**
```json
{
  "question": "What is the maximum voltage rating of TARIL power transformers?"
}
```

**Response:**
```json
{
  "answer": "1200 kV",
  "confidence_score": 0.76,
  "product_name": "Power Transformers",
  "source_url": "https://www.transformerindia.com/products-and-services/power-transformers",
  "image_url": "https://webcms.transformerindia.com/uploads/..."
}
```

**Confidence Score:** Cosine similarity from FAISS (0.0–1.0). Scores below 0.4 are flagged as low confidence in the UI.

---

## Sample Q&A Results

| Question | Answer | Score |
|---|---|---|
| Max voltage of power transformers? | 33 kV | 0.76 ✅ |
| Product for metal smelting/electrolysis? | Rectifier transformers | 0.41 ✅ |
| Furnace transformer cooling options? | Built-in snubbers, LV cooling, oil-water heat exchangers | 0.61 ✅ |
| Transformer for renewable energy? | Converter duty and rectifier transformers | 0.67 ✅ |
| Manufacturing plant locations? | Moraiya, Changodar, Odhav — India | 0.61 ✅ |

---

## Data Pipeline

### Scraping
- Source: `transformerindia.com/products-and-services/*` + `/about-us`
- Extracted: Product name, description, features, specs, application industries, images
- Products covered: Power, Furnace, Rectifier, Distribution, Reactors, Special Transformers

### Chunking
- 26 chunks total
- Each chunk stores: `text`, `title`, `image_path`, `source`, `product_name`
- Image paths linked as metadata — served directly in API response

### Embeddings
- Model: `all-MiniLM-L6-v2` (384-dim, normalized)
- FAISS `IndexFlatIP` — inner product = cosine similarity on normalized vectors
- 26 vectors indexed

### Retrieval
- Query → embed → FAISS search → top-3 chunks
- Confidence score = cosine similarity of best matching chunk

### Generation
- Model: `google/flan-t5-base`
- Context: top-3 chunk texts joined
- Prompt engineered for specific names, numbers, locations

---

## Key Design Decisions

**Why flan-t5-base?**  
Free, runs locally, no API cost, fast inference. Sufficient for factual Q&A on structured product data.

**Why FAISS over Chroma?**  
Lightweight, no server needed, persists as a single file, fast similarity search.

**Why all-MiniLM-L6-v2?**  
Best-in-class for semantic similarity at small size (80MB). Free via HuggingFace.

**Confidence Score Logic:**  
FAISS cosine similarity on normalized embeddings directly gives 0.0–1.0 range. No post-processing needed. Scores < 0.4 flagged as LOW in UI.

---

## Live Walkthrough Prep

Things I can modify on the spot:
- `top_k` value (retrieve more/fewer chunks)
- Add new chunks to knowledge base and re-index
- Change prompt engineering in `generator.py`
- Add new API endpoints
- Adjust confidence threshold for flagging

---

*Built with: Python 3.11 · FastAPI · Streamlit · HuggingFace Transformers · FAISS · BeautifulSoup*