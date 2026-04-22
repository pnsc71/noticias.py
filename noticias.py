import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
import re
import html

# 1. Design Otimizado para iPhone
st.set_page_config(page_title="Radar Elite", page_icon="📡", layout="wide")

IMAGEM_FIXA = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&h=300&q=80"

st.markdown(f"""
    <style>
    .news-card {{
        background-color: #1e212b;
        padding: 15px;
        border-radius: 12px;
        border-bottom: 4px solid #007bff;
        margin-bottom: 15px;
        height: 410px;
        overflow: hidden;
    }}
    .breaking-card {{
        background-color: #2d0a0a;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #ff4b4b;
        margin-bottom: 15px;
        height: 410px;
    }}
    .img-container img {{
        width: 100%;
        border-radius: 8px;
        object-fit: cover;
        height: 140px;
    }}
    .tag {{
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 10px;
        font-weight: bold;
        background: #333;
        color: white;
    }}
    .card-title {{
        font-size: 16px;
        font-weight: bold;
        margin-top: 10px;
        height: 55px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }}
    .card-text {{
        font-size: 13px;
        color: #bbb;
        height: 55px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. Motor de Tradução
@st.cache_data(ttl=600)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        texto_limpo = html.unescape(re.sub('<[^<]+?>', '', texto)).strip()
        return GoogleTranslator(source='en', target='pt').translate(texto_limpo[:250])
    except: return texto

# 3. Fontes de Informação (O Plantel de Luxo)
fontes = [
    # --- MUNDO & USA ---
    {"n": "New York Times", "u": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "tr": True},
    {"n": "CNN International", "u": "http://rss.cnn.com/rss/edition.rss", "tr": True},
    {"n": "BBC News", "u": "http://feeds.bbci.co.uk/news/world/rss.xml", "tr": True},
    
    # --- PORTUGAL (Geral & Rádio) ---
    {"n": "RTP Notícias", "u": "https://www.rtp.pt/noticias/rss", "tr": False},
    {"n": "Observador", "u": "https://observador.pt/feed/", "tr": False},
    {"n": "TSF", "u": "https://www.tsf.pt/rss/noticias/portugal.xml", "tr": False},
    {"n": "CNN Portugal", "u": "https://cnnportugal.iol.pt/rss", "tr": False},
    
    # --- IA & TECH ---
    {"n": "MIT Tech Review (IA)", "u": "https://www.technologyreview.com/topic/artificial-intelligence/feed/", "tr": True},
    {"n": "Pplware", "u": "https://pplware.sapo.pt/feed/", "tr": False},
    {"n": "The Ambient (HA)", "u": "https://www.the-ambient.com/rss", "tr": True},
    
    # --- FUTEBOL ---
    {"n": "A Bola", "u": "https://www.abola.pt/rss/0", "tr": False},
    {"n": "Record", "u": "https://www.record.pt/rss", "tr": False}
]

# 4. Processamento
st.title("🛰️ Radar Elite")
st.caption(f"A monitorizar {len(fontes)} fontes de referência")

all_items = []
for f in fontes:
    try:
        feed = feedparser.parse(f['u'])
        for entry in feed.entries[:2]: # Top 2 de cada fonte
            entry['fn'] = f['n']
            entry['tr'] = f['tr']
            all_items.append(entry)
    except:
        continue

# 5. Grelha Visual
cols = st.columns(2)
for i, item in enumerate(all_items):
    with cols[i % 2]:
        tit = traduzir_pt(item.title) if item['tr'] else html.unescape(item.title)
        res_raw = item.get('summary', '') or item.get('description', '')
        res = traduzir_pt(res_raw) if item['tr'] else html.unescape(res_raw)
        res = re.sub('<[^<]+?>', '', res)
        
        is_b = any(p in tit.upper() for p in ["URGENTE", "ÚLTIMA", "BREAKING", "ALERTA"])
        c_class = "breaking-card" if is_b else "news-card"
        lbl = "🚨 ALERTA" if is_b else item['fn']

        st.markdown(f"""
            <div class="{c_class}">
                <div class="img-container"><img src="{IMAGEM_FIXA}"></div>
                <span class="tag">{lbl}</span>
                <div class="card-title">{tit}</div>
                <div class="card-text">{res}</div>
                <a href="{item.link}" target="_blank" style="color:#007bff; text-decoration:none; font-weight:bold; font-size:12px;">LER MAIS →</a>
            </div>
            """, unsafe_allow_html=True)
