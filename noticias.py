import streamlit as st
import feedparser
from deep_translator import MyMemoryTranslator
import re
import html

# 1. Configuração da Página
st.set_page_config(page_title="Radar Total Pro", page_icon="📡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stExpander { border: 1px solid #30363d !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Radar Total: Portugal & Mundo")

# 2. Função de Tradução Especialista em pt-PT
@st.cache_data(ttl=600)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        # Limpa códigos HTML antes de traduzir
        texto_limpo = html.unescape(re.sub('<[^<]+?>', '', texto))
        # Traduz forçando o sotaque de Portugal
        return MyMemoryTranslator(source='en-GB', target='pt-PT').translate(texto_limpo)
    except:
        return texto

# 3. Lista de Fontes (PT e Estrangeiras)
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "cor": "🔴", "traduzir": False},
    {"nome": "RTP Notícias", "url": "https://www.rtp.pt/noticias/rss", "cor": "🔵", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "cor": "🟢", "traduzir": False},
    {"nome": "CNN (EUA)", "url": "http://rss.cnn.com/rss/edition.rss", "cor": "🇺🇸", "traduzir": True},
    {"nome": "BBC (UK)", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "cor": "🇬🇧", "traduzir": True},
    {"nome": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "cor": "🌍", "traduzir": True}
]

# 4. Construção do Dashboard
col1, col2 = st.columns(2)

for i, fonte in enumerate(fontes):
    coluna = col1 if i % 2 == 0 else col2
    with coluna:
        st.subheader(f"{fonte['cor']} {fonte['nome']}")
        feed = feedparser.parse(fonte['url'])
        
        for item in feed.entries[:5]:
            if fonte['traduzir']:
                # Processo para notícias de fora
                titulo = traduzir_pt(item.title)
                resumo = traduzir_pt(item.get('summary', ''))
            else:
                # Processo para notícias de PT (Limpeza de "lixo" da CNN/RTP)
                titulo = html.unescape(item.title)
                resumo_raw = item.get('summary', '') or item.get('description', '')
                # Descodifica símbolos e retira tags HTML
                resumo = html.unescape(resumo_raw)
                resumo = re.sub('<[^<]+?>', '', resumo)

            with st.expander(f"📌 {titulo}"):
                st.write(resumo)
                st.caption(f"🔗 [Ler notícia completa]({item.link})")
        st.write("---")
