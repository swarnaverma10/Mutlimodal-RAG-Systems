# frontend/app.py
# Run: py -m streamlit run frontend/app.py

import streamlit as st
import requests

API_URL = "https://mutlimodal-rag-systems.onrender.com"

IMAGE_MAP = {
    "Furnace Transformers":      "https://webcms.transformerindia.com/uploads/Changodar_01_4dc5abf9d5.jpg",
    "Furnace Transformer":       "https://webcms.transformerindia.com/uploads/Changodar_01_4dc5abf9d5.jpg",
    "Power Transformers":        "https://webcms.transformerindia.com/uploads/about_us_af50584e1e.png",
    "Power Transformer":         "https://webcms.transformerindia.com/uploads/about_us_af50584e1e.png",
    "Rectifier Transformers":    "https://webcms.transformerindia.com/uploads/IMG_5514_3ed4898e6a.JPG",
    "Rectifier Transformer":     "https://webcms.transformerindia.com/uploads/IMG_5514_3ed4898e6a.JPG",
    "Distribution Transformers": "https://webcms.transformerindia.com/uploads/about_us_af50584e1e.png",
    "Distribution Transformer":  "https://webcms.transformerindia.com/uploads/about_us_af50584e1e.png",
    "Special Transformers":      "https://webcms.transformerindia.com/uploads/IMG_5514_3ed4898e6a.JPG",
    "Special Transformer":       "https://webcms.transformerindia.com/uploads/IMG_5514_3ed4898e6a.JPG",
    "Reactors":                  "https://webcms.transformerindia.com/uploads/about_us_af50584e1e.png",
    "Repair and Refurbishment":  "https://webcms.transformerindia.com/uploads/about_us_af50584e1e.png",
    "Manufacturing Plants":      "https://webcms.transformerindia.com/uploads/about_us_af50584e1e.png",
}
DEFAULT_IMAGE = "https://webcms.transformerindia.com/uploads/about_us_af50584e1e.png"

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TARIL AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(99,102,241,0.15), transparent),
        radial-gradient(ellipse 60% 40% at 90% 10%, rgba(139,92,246,0.08), transparent),
        #07070c !important;
    font-family: 'Inter', sans-serif;
    color: #e2e2e9;
}

#MainMenu, footer, header { visibility: hidden; }

/* ── FULL WIDTH CONTAINER ── */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    max-width: 100% !important;
}

@media (min-width: 1400px) {
    .block-container {
        padding-left: 6rem !important;
        padding-right: 6rem !important;
    }
}

/* ── NAVBAR ── */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2.5rem;
    padding: 1rem 1.5rem;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    backdrop-filter: blur(20px);
}
.nav-logo { display: flex; align-items: center; gap: 14px; }
.nav-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 6px 20px rgba(99,102,241,0.45);
}
.nav-name { font-size: 1.05rem; font-weight: 700; color: #f5f5fa; letter-spacing: -0.3px; }
.nav-tag {
    font-size: 0.7rem; font-weight: 600; color: #a78bfa;
    background: rgba(139,92,246,0.12);
    border: 1px solid rgba(139,92,246,0.25);
    padding: 0.3rem 0.7rem; border-radius: 20px; letter-spacing: 0.4px;
    margin-left: 4px;
}
.status-pill {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.78rem; color: #a0a0b0; font-weight: 500;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 0.5rem 1rem; border-radius: 20px;
}
.dot-live {
    width: 7px; height: 7px; border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 10px rgba(34,197,94,0.9);
    animation: blink 2s infinite;
}
.dot-dead { width: 7px; height: 7px; border-radius: 50%; background: #ef4444; }
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:0.4;} }

/* ── HERO ── */
.hero-section { text-align: center; margin-bottom: 2.5rem; padding: 1rem 0; }
.hero-eyebrow {
    font-size: 0.72rem; font-weight: 600; letter-spacing: 4px;
    text-transform: uppercase; color: #a78bfa; margin-bottom: 1rem;
}
.hero-title {
    font-size: 3.2rem; font-weight: 800; color: #f5f5fa;
    letter-spacing: -1.8px; line-height: 1.1; margin-bottom: 1rem;
}
.hero-title span {
    background: linear-gradient(135deg, #6366f1 0%, #a78bfa 50%, #ec4899 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-desc {
    font-size: 1rem; color: #888; line-height: 1.7;
    max-width: 600px; margin: 0 auto; font-weight: 400;
}

/* ── SEARCH WRAPPER ── */
.search-wrapper {
    max-width: 900px;
    margin: 0 auto 2rem;
}

/* ── INPUT ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 16px !important;
    color: #f5f5fa !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 1.2rem 1.6rem !important;
    transition: all 0.25s ease !important;
    height: auto !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(99,102,241,0.7) !important;
    background: rgba(99,102,241,0.06) !important;
    box-shadow: 0 0 0 4px rgba(99,102,241,0.12), 0 8px 32px rgba(0,0,0,0.4) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.25) !important; }
.stTextInput label { display: none !important; }

/* ── BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #7c3aed) !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.95rem 2rem !important;
    width: 100% !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.35) !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #7c3aed, #8b5cf6) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(99,102,241,0.5) !important;
}
.stButton > button:disabled {
    background: rgba(255,255,255,0.06) !important;
    color: rgba(255,255,255,0.3) !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
}

/* ── RESULTS WRAPPER ── */
.results-wrapper {
    max-width: 1100px;
    margin: 2.5rem auto 0;
}

/* ── FADE IN ── */
@keyframes fadeInUp {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:translateY(0); }
}
.result-block { animation: fadeInUp 0.5s ease forwards; margin-bottom: 1.5rem; }

/* ── ANSWER CARD ── */
.answer-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2.2rem 2.5rem;
    position: relative; overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.answer-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.6), rgba(167,139,250,0.6), transparent);
}
.card-eyebrow {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: rgba(167,139,250,0.9);
    margin-bottom: 1.2rem; display: flex; align-items: center; gap: 10px;
}
.card-eyebrow::before {
    content: ''; display: inline-block;
    width: 20px; height: 2px;
    background: linear-gradient(90deg, #6366f1, #a78bfa);
    border-radius: 2px;
}
.product-chip {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.3);
    color: #c4b5fd; font-size: 0.82rem; font-weight: 600;
    padding: 0.4rem 0.95rem; border-radius: 8px; margin-bottom: 1.3rem;
}
.answer-text {
    font-size: 1.18rem; color: #e0e0ec; line-height: 1.85;
    padding-left: 1.3rem; border-left: 3px solid;
    border-image: linear-gradient(180deg, #6366f1, #a78bfa) 1;
    font-weight: 400;
}

/* ── SOURCE CARD ── */
.source-card {
    display: flex; align-items: center; gap: 12px;
    padding: 1.1rem 1.6rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    font-size: 0.88rem;
    transition: all 0.2s ease;
}
.source-card:hover {
    background: rgba(99,102,241,0.06);
    border-color: rgba(99,102,241,0.3);
}
.source-icon {
    font-size: 1.1rem;
    flex-shrink: 0;
}
.source-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: rgba(255,255,255,0.4);
    margin-right: 8px;
}
.source-card a {
    color: #a78bfa; text-decoration: none; transition: color 0.15s;
    font-weight: 500; word-break: break-all;
}
.source-card a:hover { color: #c4b5fd; text-decoration: underline; }

/* ── CONFIDENCE CARD ── */
.confidence-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.confidence-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1.5rem;
}
.confidence-label {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: rgba(167,139,250,0.9);
    display: flex; align-items: center; gap: 10px;
}
.confidence-label::before {
    content: ''; display: inline-block;
    width: 20px; height: 2px;
    background: linear-gradient(90deg, #6366f1, #a78bfa);
    border-radius: 2px;
}
.confidence-badge {
    font-size: 0.72rem; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase;
    padding: 0.4rem 0.95rem; border-radius: 8px;
}
.confidence-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 4.5rem; font-weight: 600;
    line-height: 1; margin-bottom: 1.2rem; letter-spacing: -2.5px;
}
.confidence-bar-bg {
    width: 100%; height: 10px;
    background: rgba(255,255,255,0.05);
    border-radius: 10px; overflow: hidden;
    position: relative;
}
.confidence-bar-fill {
    height: 100%; border-radius: 10px;
    transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.confidence-bar-fill::after {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: shimmer 2.5s infinite;
}
@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
.confidence-footer {
    display: flex; justify-content: space-between;
    margin-top: 0.8rem;
    font-size: 0.72rem; color: rgba(255,255,255,0.3);
    font-family: 'JetBrains Mono', monospace;
}

/* ── IMAGE CARD ── */
.image-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px; overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.image-card-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.5rem 2rem 1rem;
}
.image-card-label {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: rgba(167,139,250,0.9);
    display: flex; align-items: center; gap: 10px;
}
.image-card-label::before {
    content: ''; display: inline-block;
    width: 20px; height: 2px;
    background: linear-gradient(90deg, #6366f1, #a78bfa);
    border-radius: 2px;
}
.image-wrapper {
    padding: 0 1.5rem 1.5rem;
}
.image-wrapper img {
    width: 100% !important;
    border-radius: 14px !important;
    filter: brightness(1.05) contrast(1.08) saturate(1.05);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    transition: transform 0.4s ease;
}
.image-wrapper img:hover {
    transform: scale(1.01);
}
.img-caption {
    padding: 1.2rem 2rem 1.8rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    background: rgba(255,255,255,0.02);
}
.img-caption-label {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 2.5px;
    text-transform: uppercase; color: rgba(255,255,255,0.35);
    margin-bottom: 0.4rem;
}
.img-caption-name {
    font-size: 1.25rem; font-weight: 700; color: #f5f5fa;
    letter-spacing: -0.3px;
}

/* Streamlit image override */
[data-testid="stImage"] {
    width: 100% !important;
}
[data-testid="stImage"] img {
    width: 100% !important;
    border-radius: 14px !important;
    filter: brightness(1.05) contrast(1.08) saturate(1.05);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4);
}

/* ── EXPANDER ── */
.streamlit-expanderHeader, [data-testid="stExpander"] summary {
    background: rgba(255,255,255,0.03) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,0.5) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 0.9rem 1.4rem !important;
}
[data-testid="stExpander"] {
    border: none !important;
    background: transparent !important;
}
.streamlit-expanderContent {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 0 0 12px 12px !important;
    border-top: none !important;
}

/* ── FOOTER ── */
.app-footer {
    margin-top: 5rem; padding: 1.5rem 1rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    display: flex; justify-content: space-between; align-items: center;
    font-size: 0.75rem; color: rgba(255,255,255,0.25); letter-spacing: 0.3px;
    flex-wrap: wrap; gap: 1rem;
}
.app-footer strong { color: rgba(255,255,255,0.5); font-weight: 600; }

/* ── ALERTS / SPINNER ── */
.stSpinner > div { border-top-color: #6366f1 !important; }
.stAlert {
    border-radius: 12px !important;
    font-size: 0.9rem !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* Hide default Streamlit progress (we use custom) */
.stProgress { display: none !important; }

/* Responsive */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }
    .hero-title { font-size: 2.2rem; }
    .answer-card, .confidence-card { padding: 1.5rem 1.3rem; }
    .image-card-header, .image-wrapper, .img-caption { padding-left: 1.2rem; padding-right: 1.2rem; }
    .confidence-number { font-size: 3.2rem; }
    .answer-text { font-size: 1.05rem; }
}
</style>
""", unsafe_allow_html=True)

# ── BACKEND CHECK ─────────────────────────────────────────────────────────────
try:
    ping = requests.get(f"{API_URL}/health", timeout=2)
    backend_ok = ping.status_code == 200
    status_html = '<span class="dot-live"></span> System online'
except Exception:
    backend_ok = False
    status_html = '<span class="dot-dead"></span> Backend offline'

# ── NAVBAR ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="navbar">
    <div class="nav-logo">
        <div class="nav-icon">⚡</div>
        <div class="nav-name">TARIL Assistant</div>
        <span class="nav-tag">RAG · AI</span>
    </div>
    <div class="status-pill">{status_html}</div>
</div>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-eyebrow">Multimodal RAG System</div>
    <div class="hero-title">Ask anything about<br><span>TARIL Transformers</span></div>
    <div class="hero-desc">Semantic search over TARIL's product knowledge base — grounded answers with product images, source citations, and confidence scoring.</div>
</div>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# ── SEARCH (centered, max-width) ─────────────────────────────────────────────
search_col_l, search_col_c, search_col_r = st.columns([1, 3, 1])
with search_col_c:
    question = st.text_input(
        "query",
        placeholder="e.g. What is the maximum voltage rating of TARIL power transformers?",
        label_visibility="collapsed",
        key="query_box"
    )
    ask = st.button("⚡  Ask TARIL Assistant", disabled=not backend_ok, key="ask_btn")

# ── QUERY ────────────────────────────────────────────────────────────────────
if ask and question.strip():
    with st.spinner("Searching knowledge base..."):
        try:
            resp   = requests.post(f"{API_URL}/query", json={"question": question}, timeout=60)
            result = resp.json()
            st.session_state.last_result = {"question": question, "data": result}
        except requests.exceptions.ConnectionError:
            st.error("Backend not running. Start: py -m uvicorn backend.main:app --port 8000")
        except Exception as e:
            st.error(f"Error: {e}")
elif ask and not question.strip():
    st.warning("Please type a question first.")

# ── RESULTS ───────────────────────────────────────────────────────────────────
if st.session_state.last_result:
    result       = st.session_state.last_result["data"]
    answer       = result.get("answer", "No answer generated.")
    score        = float(result.get("confidence_score", 0.0))
    product_name = result.get("product_name", "")
    source_url   = result.get("source_url", "")
    img_url      = IMAGE_MAP.get(product_name, DEFAULT_IMAGE)

    if score >= 0.70:
        score_color = "#22c55e"
        score_bg    = "rgba(34,197,94,0.12)"
        score_label = "HIGH MATCH"
    elif score >= 0.50:
        score_color = "#f59e0b"
        score_bg    = "rgba(245,158,11,0.12)"
        score_label = "GOOD MATCH"
    else:
        score_color = "#ef4444"
        score_bg    = "rgba(239,68,68,0.12)"
        score_label = "LOW MATCH"

    # Wrap all results in a centered max-width container
    res_l, res_c, res_r = st.columns([0.5, 6, 0.5])

    with res_c:
        # ─── 1. GENERATED ANSWER ─────────────────────────────────────────
        product_html = f'<div class="product-chip">📦 {product_name}</div>' if product_name else ""
        st.markdown(f"""
        <div class="result-block">
            <div class="answer-card">
                <div class="card-eyebrow">Generated Answer</div>
                {product_html}
                <div class="answer-text">{answer}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ─── 2. SOURCE URL ───────────────────────────────────────────────
        if source_url:
            st.markdown(f"""
            <div class="result-block">
                <div class="source-card">
                    <span class="source-icon">📎</span>
                    <span class="source-label">Source</span>
                    <a href="{source_url}" target="_blank">{source_url}</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ─── 3. CONFIDENCE SCORE ─────────────────────────────────────────
        score_pct = min(score, 1.0) * 100
        st.markdown(f"""
        <div class="result-block">
            <div class="confidence-card">
                <div class="confidence-header">
                    <div class="confidence-label">Confidence Score</div>
                    <div class="confidence-badge" style="color:{score_color}; background:{score_bg}; border:1px solid {score_color}40;">
                        {score_label}
                    </div>
                </div>
                <div class="confidence-number" style="color:{score_color};">{score:.0%}</div>
                <div class="confidence-bar-bg">
                    <div class="confidence-bar-fill" style="width:{score_pct}%; background: linear-gradient(90deg, {score_color}, {score_color}cc);"></div>
                </div>
                <div class="confidence-footer">
                    <span>0%</span>
                    <span>cosine similarity · FAISS</span>
                    <span>100%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ─── 4. PRODUCT IMAGE ────────────────────────────────────────────
        # FIX: Render the card header and image using a container approach.
        # The card shell (open + header) is rendered first, then st.image()
        # is used for the actual image (required for Streamlit to handle
        # remote URLs), then the caption and closing tags are rendered in
        # a single st.markdown() call with unsafe_allow_html=True.

        st.markdown("""
        <div class="result-block">
            <div class="image-card">
                <div class="image-card-header">
                    <div class="image-card-label">Product Image</div>
                </div>
                <div class="image-wrapper">
        """, unsafe_allow_html=True)

        st.image(img_url, use_container_width=True)

        # Build caption HTML only when product_name exists, then close all
        # open divs in ONE st.markdown() call so no raw HTML leaks as text.
        if product_name:
            closing_html = f"""
                </div>
                <div class="img-caption">
                    <div class="img-caption-label">Product</div>
                    <div class="img-caption-name">{product_name}</div>
                </div>
            </div>
        </div>
            """
        else:
            closing_html = """
                </div>
            </div>
        </div>
            """

        st.markdown(closing_html, unsafe_allow_html=True)

        # ─── 5. RAW API RESPONSE ─────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🔧 View raw API response"):
            st.json(result)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <span><strong>TARIL Multimodal RAG</strong> · Swarna Verma</span>
    <span>FAISS + flan-t5-base + HuggingFace + FastAPI</span>
</div>
""", unsafe_allow_html=True)