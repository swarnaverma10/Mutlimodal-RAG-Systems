# frontend/app.py — Purple Black Theme + Fixed Health Check + Animations

import streamlit as st
import requests

st.set_page_config(
    page_title="TRIL Product Assistant",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

.stApp { background: #08050f; min-height: 100vh; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; padding-bottom: 3rem !important; max-width: 900px !important; }

@keyframes floatOrb1 {
    0%,100% { transform: translate(0,0) scale(1); opacity:0.6; }
    33%      { transform: translate(30px,-20px) scale(1.05); opacity:0.8; }
    66%      { transform: translate(-20px,15px) scale(0.95); opacity:0.5; }
}
@keyframes floatOrb2 {
    0%,100% { transform: translate(0,0) scale(1); opacity:0.4; }
    50%      { transform: translate(-25px,-30px) scale(1.08); opacity:0.65; }
}
@keyframes fadeInUp {
    from { opacity:0; transform:translateY(22px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes gradShift {
    0%,100% { background-position: 0% 50%; }
    50%      { background-position: 100% 50%; }
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:0.45; transform:scale(0.82); }
}

.hero {
    background: linear-gradient(135deg, #0f0a1e 0%, #130d24 60%, #0a0818 100%);
    border-bottom: 1px solid rgba(139,92,246,0.15);
    padding: 3.5rem 3rem 2.8rem;
    margin: 0 -1rem 2.5rem -1rem;
    position: relative;
    overflow: hidden;
    animation: fadeInUp 0.7s ease both;
}
.orb1 {
    position: absolute; top: -120px; right: -80px;
    width: 420px; height: 420px;
    background: radial-gradient(circle, rgba(139,92,246,0.13) 0%, transparent 65%);
    border-radius: 50%;
    animation: floatOrb1 8s ease-in-out infinite;
}
.orb2 {
    position: absolute; bottom: -100px; left: 10%;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(167,139,250,0.08) 0%, transparent 65%);
    border-radius: 50%;
    animation: floatOrb2 11s ease-in-out infinite;
}
.orb3 {
    position: absolute; top: 30%; left: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(109,40,217,0.07) 0%, transparent 70%);
    border-radius: 50%;
    animation: floatOrb1 14s ease-in-out infinite reverse;
}
.hero-eyebrow {
    font-family: 'Outfit', sans-serif;
    font-size: 0.7rem; font-weight: 600;
    letter-spacing: 5px; text-transform: uppercase;
    color: #a78bfa; margin-bottom: 1.2rem;
    display: flex; align-items: center; gap: 10px;
    position: relative; animation: fadeInUp 0.7s 0.1s ease both;
}
.hero-eyebrow::before {
    content: ''; display: inline-block;
    width: 28px; height: 1px;
    background: linear-gradient(90deg, #7c3aed, #a78bfa);
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 4rem; font-weight: 800; color: #ffffff;
    margin: 0 0 0.7rem 0; letter-spacing: -1px; line-height: 1.05;
    position: relative; animation: fadeInUp 0.7s 0.2s ease both;
}
.hero-title span {
    background: linear-gradient(135deg, #8b5cf6, #a78bfa, #c4b5fd, #8b5cf6);
    background-size: 200% 200%;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; animation: gradShift 4s ease infinite;
}
.hero-desc {
    font-family: 'Outfit', sans-serif; font-size: 0.95rem;
    color: rgba(255,255,255,0.35); margin: 0; font-weight: 300;
    max-width: 500px; line-height: 1.7;
    position: relative; animation: fadeInUp 0.7s 0.3s ease both;
}
.hero-stats {
    display: flex; gap: 2.5rem;
    margin-top: 2.2rem; padding-top: 2rem;
    border-top: 1px solid rgba(139,92,246,0.12);
    position: relative; animation: fadeInUp 0.7s 0.4s ease both;
}
.stat-num {
    font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 800;
    background: linear-gradient(135deg, #8b5cf6, #c4b5fd);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1;
}
.stat-label {
    font-family: 'Outfit', sans-serif; font-size: 0.65rem;
    color: rgba(255,255,255,0.25); letter-spacing: 2.5px;
    text-transform: uppercase; margin-top: 4px;
}
.status-bar {
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 2rem; font-family: 'Outfit', sans-serif;
    font-size: 0.75rem; color: rgba(255,255,255,0.28);
    animation: fadeInUp 0.5s 0.5s ease both;
}
.dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #22c55e; box-shadow: 0 0 10px rgba(34,197,94,0.7);
    animation: pulse 2s infinite;
}
.dot-off { background: #ef4444; box-shadow: 0 0 8px rgba(239,68,68,0.6); animation: none; }
.section-label {
    font-family: 'Outfit', sans-serif; font-size: 0.65rem; font-weight: 600;
    letter-spacing: 3.5px; text-transform: uppercase;
    color: rgba(167,139,250,0.45); margin-bottom: 0.8rem; display: block;
}
.stButton > button {
    background: rgba(139,92,246,0.08) !important;
    color: rgba(196,181,253,0.75) !important;
    font-family: 'Outfit', sans-serif !important; font-weight: 500 !important;
    font-size: 0.82rem !important; border: 1px solid rgba(139,92,246,0.2) !important;
    border-radius: 8px !important; padding: 0.55rem 1rem !important;
    width: 100% !important; transition: all 0.2s ease !important;
    letter-spacing: 0.2px !important; text-transform: none !important;
}
.stButton > button:hover {
    background: rgba(139,92,246,0.2) !important;
    border-color: rgba(139,92,246,0.55) !important;
    color: #c4b5fd !important; transform: translateY(-2px) !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.2) !important;
}
.stTextInput > div > div > input {
    background: #100d1e !important; border: 1px solid rgba(139,92,246,0.22) !important;
    border-radius: 10px !important; color: #e8e4f5 !important;
    font-family: 'Outfit', sans-serif !important; font-size: 1rem !important;
    padding: 0.9rem 1.4rem !important; transition: all 0.25s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
    background: #120f20 !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.18) !important; }
.answer-card {
    background: linear-gradient(135deg, #0f0a1e 0%, #110d20 100%);
    border: 1px solid rgba(139,92,246,0.18); border-radius: 16px;
    padding: 2rem 2.2rem; margin-top: 2rem;
    box-shadow: 0 4px 40px rgba(109,40,217,0.1);
    animation: fadeInUp 0.5s ease both;
}
.card-label {
    font-family: 'Outfit', sans-serif; font-size: 0.63rem; font-weight: 600;
    letter-spacing: 3.5px; text-transform: uppercase;
    color: rgba(167,139,250,0.35); margin-bottom: 1rem;
}
.product-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(139,92,246,0.12); border: 1px solid rgba(139,92,246,0.3);
    border-radius: 6px; padding: 0.28rem 0.85rem;
    font-family: 'Outfit', sans-serif; font-size: 0.8rem; font-weight: 600;
    color: #a78bfa; margin-bottom: 1.1rem;
}
.answer-body {
    font-family: 'Outfit', sans-serif; font-size: 1rem;
    color: rgba(255,255,255,0.78); line-height: 1.8; font-weight: 300;
    border-left: 2px solid #7c3aed; padding-left: 1.2rem; margin: 0 0 1.4rem 0;
}
.meta-card {
    background: #0c0918; border: 1px solid rgba(139,92,246,0.1);
    border-radius: 12px; padding: 1.4rem 1.5rem;
    animation: fadeInUp 0.5s 0.1s ease both;
}
.score-big {
    font-family: 'Syne', sans-serif; font-size: 3rem; font-weight: 800;
    line-height: 1; letter-spacing: -1px; margin-bottom: 0.2rem;
}
.score-sublabel {
    font-family: 'Outfit', sans-serif; font-size: 0.67rem;
    color: rgba(255,255,255,0.22); letter-spacing: 2.5px;
    text-transform: uppercase; margin-bottom: 1rem;
}
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #a78bfa) !important;
    border-radius: 10px !important;
}
.stProgress > div > div > div {
    background: rgba(139,92,246,0.1) !important;
    border-radius: 10px !important; height: 5px !important;
}
.img-wrap {
    border-radius: 8px; overflow: hidden;
    border: 1px solid rgba(139,92,246,0.12); margin-top: 0.4rem;
}
.streamlit-expanderHeader {
    font-family: 'Outfit', sans-serif !important; font-size: 0.75rem !important;
    color: rgba(167,139,250,0.3) !important; background: transparent !important;
}
.stSpinner > div { border-top-color: #7c3aed !important; }
.stAlert { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

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
    "Products and Services":     "https://webcms.transformerindia.com/uploads/about_us_af50584e1e.png",
}
DEFAULT_IMAGE = "https://webcms.transformerindia.com/uploads/about_us_af50584e1e.png"

SAMPLE_QUESTIONS = [
    "What is a furnace transformer used for?",
    "Explain TARIL power transformers",
    "What are rectifier transformers?",
    "Tell me about special transformers",
    "What does TARIL manufacture?",
    "What are shunt reactors used for?",
]

API_URL = "http://127.0.0.1:8000"

st.markdown("""
<div class="hero">
    <div class="orb1"></div><div class="orb2"></div><div class="orb3"></div>
    <div class="hero-eyebrow">AI-Powered Product Intelligence</div>
    <div class="hero-title">TRIL <span>Product</span><br>Assistant</div>
    <p class="hero-desc">Instant grounded answers about TARIL transformer products — powered by semantic search and local AI generation.</p>
    <div class="hero-stats">
        <div class="stat-item"><div class="stat-num">24</div><div class="stat-label">Knowledge Chunks</div></div>
        <div class="stat-item"><div class="stat-num">7</div><div class="stat-label">Product Categories</div></div>
        <div class="stat-item"><div class="stat-num">RAG</div><div class="stat-label">Architecture</div></div>
        <div class="stat-item"><div class="stat-num">FREE</div><div class="stat-label">Open Source</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── BACKEND STATUS — tries /health first, then / ──────────────────────────────
backend_ok = False
try:
    ping = requests.get(f"{API_URL}/health", timeout=2)
    backend_ok = ping.status_code == 200
except Exception:
    try:
        ping = requests.get(f"{API_URL}/", timeout=2)
        backend_ok = ping.status_code == 200
    except Exception:
        backend_ok = False

if backend_ok:
    st.markdown('<div class="status-bar"><div class="dot"></div> Backend connected — RAG system ready</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="status-bar"><div class="dot dot-off"></div> Backend offline — run: <code>py -m uvicorn backend.main:app --port 8000</code></div>', unsafe_allow_html=True)

if "selected_q" not in st.session_state:
    st.session_state.selected_q = ""

st.markdown('<span class="section-label">Try a sample question</span>', unsafe_allow_html=True)
cols = st.columns(3)
for i, q in enumerate(SAMPLE_QUESTIONS):
    with cols[i % 3]:
        label = q if len(q) <= 36 else q[:34] + "…"
        if st.button(label, key=f"sq_{i}", help=q, use_container_width=True):
            st.session_state.selected_q = q
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<span class="section-label">Ask your question</span>', unsafe_allow_html=True)

question = st.text_input(
    "", value=st.session_state.selected_q,
    placeholder="e.g. What is a furnace transformer used for?",
    label_visibility="collapsed", key="query_box"
)

ask = st.button("⚡  Search Knowledge Base", key="ask_btn", use_container_width=True)

if ask and question.strip():
    if not backend_ok:
        st.error("❌ Backend offline. Run: py -m uvicorn backend.main:app --port 8000")
    else:
        with st.spinner("Searching TARIL knowledge base..."):
            try:
                resp = requests.post(f"{API_URL}/query", json={"question": question}, timeout=60)
                result = resp.json()

                answer       = result.get("answer", "No answer generated.")
                score        = float(result.get("confidence_score", result.get("confidence", 0.0)))
                product_name = result.get("product_name", "")
                source_url   = result.get("source_url", result.get("source", ""))
                img_url      = IMAGE_MAP.get(product_name, DEFAULT_IMAGE)

                score_color = "#22c55e" if score >= 0.70 else ("#a78bfa" if score >= 0.50 else "#64748b")
                score_label = "High Match" if score >= 0.70 else ("Good Match" if score >= 0.50 else "Low Match")

                st.markdown('<div class="answer-card">', unsafe_allow_html=True)
                st.markdown('<p class="card-label">Generated Answer</p>', unsafe_allow_html=True)
                if product_name:
                    st.markdown(f'<div class="product-pill">📦 {product_name}</div>', unsafe_allow_html=True)
                st.markdown(f'<p class="answer-body">{answer}</p>', unsafe_allow_html=True)
                if source_url and source_url not in ("", "no-source"):
                    st.markdown(
                        f'<div style="font-family:Outfit,sans-serif;font-size:0.72rem;color:rgba(255,255,255,0.18);'
                        f'border-top:1px solid rgba(139,92,246,0.1);padding-top:1rem;margin-top:0.2rem;">'
                        f'📎 Source: <a href="{source_url}" target="_blank" style="color:rgba(167,139,250,0.6);text-decoration:none;">{source_url}</a></div>',
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown('<div class="meta-card">', unsafe_allow_html=True)
                    st.markdown('<p class="card-label">Confidence</p>', unsafe_allow_html=True)
                    st.markdown(f'<div class="score-big" style="color:{score_color};">{score:.0%}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="score-sublabel">{score_label}</div>', unsafe_allow_html=True)
                    st.progress(min(score, 1.0))
                    st.markdown('</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="meta-card">', unsafe_allow_html=True)
                    st.markdown('<p class="card-label">Product Image</p>', unsafe_allow_html=True)
                    st.markdown('<div class="img-wrap">', unsafe_allow_html=True)
                    st.image(img_url, caption=product_name, use_container_width=True)
                    st.markdown('</div></div>', unsafe_allow_html=True)

                with st.expander("🔍 Raw API Response"):
                    st.json(result)

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot reach backend. Run: py -m uvicorn backend.main:app --port 8000")
            except Exception as e:
                st.error(f"Error: {e}")

elif ask and not question.strip():
    st.warning("⚠️ Please type a question first.")

st.markdown("""
<div style="margin-top:4rem;padding-top:1.5rem;border-top:1px solid rgba(139,92,246,0.08);
text-align:center;font-family:'Outfit',sans-serif;font-size:0.7rem;
color:rgba(255,255,255,0.12);letter-spacing:1.5px;">
TRIL PRODUCT ASSISTANT &nbsp;·&nbsp; MULTIMODAL RAG &nbsp;·&nbsp;
HUGGINGFACE + FAISS + FASTAPI + STREAMLIT &nbsp;·&nbsp; SWARNA VERMA
</div>
""", unsafe_allow_html=True)