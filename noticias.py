import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
import re
import html

# 1. Configuração de Estilo "Revista"
st.set_page_config(page_title="Radar News Pro", page_icon="📰", layout="wide")

st.markdown("""
    <style>
    /* Estilo dos Cards de Notícias */
    .news-card {
        background-color: #1e212b;
        padding: 20px;
        border-radius: 15px;
        border-bottom: 4px solid #007bff;
        margin-bottom: 20px;
        min-height: 200px;
    }
    .source-tag {
        font-size: 12px;
        text-transform: uppercase;
        color: #007bff;
        font-weight: bold;
    }
    .briefing-top {
        background: linear-gradient(90deg, #007bff, #00d4ff);
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Tradução Otimizada
@st.cache_data(ttl=300)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        texto_limpo = html.unescape(re.sub('<[^<]+?>', '', texto)).strip()
        return GoogleTranslator(source='en', target='pt').translate(texto_limpo)
    except:
        return texto

# 3. Fontes
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "tag": "MUNDO", "traduzir": False},
    {"nome": "RTP Notícias", "url": "https://www.rtp.pt/noticias/rss", "tag": "PAÍS", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "tag": "TECH", "traduzir": False},
    {"nome": "CNN EUA", "url": "http://rss.cnn.com/rss/edition.rss", "tag": "USA", "traduzir": True}
]

# --- 4. O TEU BRIEFING DE ENTRADA ---
st.title("🛰️ Radar Intelligence")

# Preparar o resumo rápido
briefing_itens = []
for f in fontes:
    feed = feedparser.parse(f['url'])
    if feed.entries:
        tit = traduzir_pt(feed.entries[0].title) if f['traduzir'] else html.unescape(feed.entries[0].title)
        briefing_itens.append(f"• **{f['tag']}**: {tit}")

st.markdown(f"""
    <div class="briefing-top">
        <h3>🚀 Resumo Rápido</h3>
        {"<br>".join(briefing_itens)}
    </div>
    """, unsafe_allow_html=True)

# --- 5. GRELHA VISUAL (Tipo Stories/Cards) ---
st.subheader("🔥 Últimas Horas")

# Criar colunas para os cards
cols = st.columns(2)

for idx, f in enumerate(fontes):
    col = cols[idx % 2]
    feed = feedparser.parse(f['url'])
    
    with col:
        for item in feed.entries[:3]:
            titulo = traduzir_pt(item.title) if f['traduzir'] else html.unescape(item.title)
            resumo = traduzir_pt(item.get('summary', '')) if f['traduzir'] else html.unescape(item.get('summary', '') or item.get('description', ''))
            resumo = re.sub('<[^<]+?>', '', resumo)[:150] + "..." # Limita o texto para o card não ficar gigante

            st.markdown(f"""
                <div class="news-card">
                    <span class="source-tag">{f['nome']} | {f['tag']}</span>
                    <h4>{titulo}</h4>
                    <p style="font-size: 14px; color: #ccc;">{resumo}</p>
                    <a href="{item.link}" target="_blank" style="color: #00d4ff; text-decoration: none; font-weight: bold;">Ler mais →</a>
                </div>
                """, unsafe_allow_html=True)
