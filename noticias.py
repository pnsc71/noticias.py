import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
import re
import html

# 1. Configuração de Página
st.set_page_config(page_title="Radar Pro", page_icon="📡", layout="wide")

# Estilo para leitura limpa
st.markdown("""
    <style>
    .briefing-box {
        background-color: #1e212b;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 O Teu Radar: Portugal & Mundo")

# 2. Funções de Tradução e Limpeza
@st.cache_data(ttl=300)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        texto_limpo = html.unescape(re.sub('<[^<]+?>', '', texto)).strip()
        return GoogleTranslator(source='en', target='pt').translate(texto_limpo)
    except:
        return texto

# 3. Fontes Configuradas
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "traduzir": False},
    {"nome": "RTP Notícias", "url": "https://www.rtp.pt/noticias/rss", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "traduzir": False},
    {"nome": "CNN (EUA)", "url": "http://rss.cnn.com/rss/edition.rss", "traduzir": True},
    {"nome": "BBC (UK)", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "traduzir": True}
]

# --- 4. O BRIEFING "ABRIR E LER" ---
st.subheader("🤖 Resumo Inteligente")

resumo_texto = ""
# Vamos buscar a notícia principal de cada fonte para o resumo do topo
for fonte in fontes:
    feed = feedparser.parse(fonte['url'])
    if feed.entries:
        tit_original = feed.entries[0].title
        tit_final = traduzir_pt(tit_original) if fonte['traduzir'] else html.unescape(tit_original)
        resumo_texto += f"**{fonte['nome']}**: {tit_final}  \n"

# Mostra o resumo num bloco destacado
st.markdown(f"""<div class="briefing-box">{resumo_texto}</div>""", unsafe_allow_html=True)

st.divider()

# --- 5. GRELHA COMPLETA ---
col1, col2 = st.columns(2)
for i, fonte in enumerate(fontes):
    coluna = col1 if i % 2 == 0 else col2
    with coluna:
        st.write(f"### {fonte['nome']}")
        feed = feedparser.parse(fonte['url'])
        
        for item in feed.entries[:5]:
            if fonte['traduzir']:
                titulo = traduzir_pt(item.title)
                resumo = traduzir_pt(item.get('summary', ''))
            else:
                titulo = html.unescape(item.title)
                resumo_raw = item.get('summary', '') or item.get('description', '')
                resumo = html.unescape(resumo_raw)
                resumo = re.sub('<[^<]+?>', '', resumo)

            with st.expander(f"📌 {titulo}"):
                st.write(resumo)
                st.caption(f"[Notícia completa]({item.link})")
        st.write("---")
