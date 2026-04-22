import streamlit as st
import feedparser
from deep_translator import MyMemoryTranslator
import re

st.set_page_config(page_title="Radar Portugal Pro", page_icon="📡", layout="wide")
st.title("📡 Radar Mundial (Português de Portugal)")

@st.cache_data(ttl=600)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        texto_limpo = re.sub('<[^<]+?>', '', texto)
        # Aqui está a correção: source='en-GB' em vez de 'auto'
        traducao = MyMemoryTranslator(source='en-GB', target='pt-PT').translate(texto_limpo)
        return traducao
    except:
        return texto

fontes = [
    {"nome": "CNN (EUA)", "url": "http://rss.cnn.com/rss/edition.rss", "cor": "🔴"},
    {"nome": "BBC (UK)", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "cor": "⚪"},
    {"nome": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "cor": "🟠"}
]

col1, col2 = st.columns(2)
for i, fonte in enumerate(fontes):
    coluna = col1 if i % 2 == 0 else col2
    with coluna:
        st.subheader(f"{fonte['cor']} {fonte['nome']}")
        feed = feedparser.parse(fonte['url'])
        for item in feed.entries[:5]:
            titulo = traduzir_pt(item.title)
            with st.expander(f"📌 {titulo}"):
                resumo = traduzir_pt(item.get('summary', ''))
                st.write(resumo)
                st.markdown(f"[🔗 Ver original]({item.link})")
