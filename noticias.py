import html
import streamlit as st
import feedparser
from deep_translator import MyMemoryTranslator
import re

st.set_page_config(page_title="Radar Total", page_icon="📡", layout="wide")
st.title("📡 Radar Total: Portugal & Mundo")

# Função de Tradução (apenas para fontes estrangeiras)
@st.cache_data(ttl=600)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        texto_limpo = re.sub('<[^<]+?>', '', texto)
        return MyMemoryTranslator(source='en-GB', target='pt-PT').translate(texto_limpo)
    except:
        return texto

# --- DEFINIÇÃO DAS FONTES ---
# 'traduzir': True para as de fora, False para as de cá
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "cor": "🔴", "traduzir": False},
    {"nome": "RTP Notícias", "url": "https://www.rtp.pt/noticias/rss", "cor": "🔵", "traduzir": False},
    {"nome": "Pplware (Tech)", "url": "https://pplware.sapo.pt/feed/", "cor": "🟢", "traduzir": False},
    {"nome": "CNN (EUA)", "url": "http://rss.cnn.com/rss/edition.rss", "cor": "🇺🇸", "traduzir": True},
    {"nome": "BBC (UK)", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "cor": "🇬🇧", "traduzir": True},
    {"nome": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "cor": "🌍", "traduzir": True}
]

# --- GRELHA DE EXIBIÇÃO ---
col1, col2 = st.columns(2)

for i, fonte in enumerate(fontes):
    coluna = col1 if i % 2 == 0 else col2
    with coluna:
        st.subheader(f"{fonte['cor']} {fonte['nome']}")
        feed = feedparser.parse(fonte['url'])
        
        for item in feed.entries[:5]:
            # Lógica: Traduz se necessário, caso contrário usa o original
            if fonte['traduzir']:
                titulo = traduzir_pt(item.title)
                resumo = traduzir_pt(item.get('summary', ''))
            else:
                titulo = item.title
                resumo = item.get('summary', '') or item.get('description', '')
                # Limpa HTML básico das notícias nacionais
                resumo = re.sub('<[^<]+?>', '', resumo)

            with st.expander(f"📌 {titulo}"):
                st.write(resumo)
                st.markdown(f"[🔗 Ver notícia]({item.link})")
        st.write("---")
