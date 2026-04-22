import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
import re
import html

# 1. Configuração e Design Mobile-First
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
        height: 420px; /* Altura fixa para manter a grelha alinhada */
        overflow: hidden;
    }}
    .breaking-card {{
        background-color: #2d0a0a;
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #ff4b4b;
        margin-bottom: 15px;
        height: 420px;
        overflow: hidden;
    }}
    .img-container img {{
        width: 100%;
        border-radius: 8px;
        margin-bottom: 10px;
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
        height: 60px; /* Força o título a ocupar 3 linhas no máximo */
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }}
    .card-text {{
        font-size: 13px;
        color: #bbb;
        height: 60px; /* Limita o resumo para não empurrar o card */
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        margin-bottom: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 2. Motor de Tradução
@st.cache_data(ttl=300)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        texto_limpo = html.unescape(re.sub('<[^<]+?>', '', texto)).strip()
        return GoogleTranslator(source='en', target='pt').translate(texto_limpo)
    except: return texto

# 3. Fontes
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "traduzir": False},
    {"nome": "A Bola", "url": "https://www.abola.pt/rss/0", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "traduzir": False},
    {"nome": "Público", "url": "https://www.publico.pt/rss/politica", "traduzir": False},
    {"nome": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "traduzir": True}
]

# 4. Título
st.title("🛰️ Radar Elite")

# 5. Agregação e Grelha
all_items = []
for f in fontes:
    feed = feedparser.parse(f['url'])
    for entry in feed.entries[:4]:
        entry['fonte_nome'] = f['nome']
        entry['precisa_traducao'] = f['traduzir']
        all_items.append(entry)

cols = st.columns(2)
for i, item in enumerate(all_items):
    col_idx = i % 2
    with cols[col_idx]:
        titulo = traduzir_pt(item.title) if item['precisa_traducao'] else html.unescape(item.title)
        resumo_raw = item.get('summary', '') or item.get('description', '')
        resumo = traduzir_pt(resumo_raw) if item['precisa_traducao'] else html.unescape(resumo_raw)
        resumo = re.sub('<[^<]+?>', '', resumo)
        
        palavras_alerta = ["URGENTE", "ÚLTIMA HORA", "BOMBA", "BREAKING"]
        is_breaking = any(p in titulo.upper() for p in palavras_alerta)
        card_class = "breaking-card" if is_breaking else "news-card"
        label = "🚨 URGENTE" if is_breaking else item['fonte_nome']

        st.markdown(f"""
            <div class="{card_class}">
                <div class="img-container">
                    <img src="{IMAGEM_FIXA}">
                </div>
                <span class="tag">{label}</span>
                <div class="card-title">{titulo}</div>
                <div class="card-text">{resumo}</div>
                <a href="{item.link}" target="_blank" style="color: #007bff; text-decoration: none; font-size: 13px; font-weight: bold;">LER MAIS →</a>
            </div>
            """, unsafe_allow_html=True)
