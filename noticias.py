import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
import re
import html

# 1. Configuração e Design do Dashboard
st.set_page_config(page_title="Radar Elite", page_icon="📡", layout="wide")

# Imagem fixa para consistência
IMAGEM_FIXA = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&h=300&q=80"

st.markdown(f"""
    <style>
    .news-card {{
        background-color: #1e212b;
        padding: 20px;
        border-radius: 15px;
        border-bottom: 4px solid #007bff;
        margin-bottom: 20px;
        min-height: 380px;
    }}
    .breaking-card {{
        background-color: #2d0a0a;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #ff4b4b;
        margin-bottom: 20px;
        min-height: 380px;
    }}
    .img-container img {{
        width: 100%;
        border-radius: 10px;
        margin-bottom: 15px;
        object-fit: cover;
        height: 160px;
    }}
    .tag {{
        padding: 4px 10px;
        border-radius: 5px;
        font-size: 11px;
        font-weight: bold;
        background: #333;
        color: white;
        text-transform: uppercase;
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

# 3. Fontes de Dados
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "traduzir": False},
    {"nome": "A Bola", "url": "https://www.abola.pt/rss/0", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "traduzir": False},
    {"nome": "Público", "url": "https://www.publico.pt/rss/politica", "traduzir": False},
    {"nome": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "traduzir": True}
]

# 4. Título Principal (Sem filtros)
st.title("🛰️ Radar Elite")
st.write("### As tuas notícias em tempo real")
st.divider()

# 5. Agregação Direta
all_items = []
for f in fontes:
    feed = feedparser.parse(f['url'])
    for entry in feed.entries[:4]: # 4 notícias de cada fonte para não ficar gigante
        entry['fonte_nome'] = f['nome']
        entry['precisa_traducao'] = f['traduzir']
        all_items.append(entry)

# 6. Exibição em Grelha
cols = st.columns(2)
for i, item in enumerate(all_items):
    col_idx = i % 2
    with cols[col_idx]:
        # Processamento
        titulo = traduzir_pt(item.title) if item['precisa_traducao'] else html.unescape(item.title)
        resumo_raw = item.get('summary', '') or item.get('description', '')
        resumo = traduzir_pt(resumo_raw[:200]) if item['precisa_traducao'] else html.unescape(resumo_raw[:200])
        resumo = re.sub('<[^<]+?>', '', resumo)[:120] + "..."
        
        # Alerta Breaking News
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
                <h4 style="margin-top:12px; min-height: 50px; font-size: 18px;">{titulo}</h4>
                <p style="font-size: 14px; color: #bbb;">{resumo}</p>
                <a href="{item.link}" target="_blank" style="color: #007bff; text-decoration: none; font-weight: bold;">Ler mais →</a>
            </div>
            """, unsafe_allow_html=True)
