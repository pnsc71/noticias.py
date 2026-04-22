import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
import re

# 1. Configuração e Estilo
st.set_page_config(page_title="Radar Mundial Pro", page_icon="📡", layout="wide")

# CSS para dar um estilo mais moderno
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stExpander { border: 1px solid #30363d !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📡 Radar Mundial Inteligente")

# 2. Funções de Apoio
@st.cache_data(ttl=600) # Guarda as traduções por 10 min para ser mais rápido
def traduzir(texto):
    if not texto: return ""
    try:
        # Limpa tags HTML antes de traduzir
        texto_limpo = re.sub('<[^<]+?>', '', texto)
        return GoogleTranslator(source='auto', target='pt').translate(texto_limpo)
    except:
        return texto

# 3. Barra de Pesquisa e Configurações
with st.sidebar:
    st.header("🔍 Filtros")
    termo_pesquisa = st.text_input("Procurar no mundo (ex: Crypto, Futebol...)", "")
    st.markdown("---")
    st.info("As notícias são traduzidas automaticamente de fontes globais.")

# 4. Fontes com cores de destaque
fontes = [
    {"nome": "CNN (EUA)", "url": "http://rss.cnn.com/rss/edition.rss", "cor": "🔴"},
    {"nome": "BBC (UK)", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "cor": "⚪"},
    {"nome": "RTP (PT)", "url": "https://www.rtp.pt/noticias/rss", "cor": "🔵"},
    {"nome": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "cor": "🟠"}
]

# 5. Motor de Exibição
col1, col2 = st.columns(2)
contador = 0

for fonte in fontes:
    coluna = col1 if contador % 2 == 0 else col2
    
    with coluna:
        st.subheader(f"{fonte['cor']} {fonte['nome']}")
        feed = feedparser.parse(fonte['url'])
        
        # Filtra por termo de pesquisa se houver
        noticias = [n for n in feed.entries if termo_pesquisa.lower() in n.title.lower() or termo_pesquisa == ""]
        
        for item in noticias[:5]:
            titulo_pt = traduzir(item.title)
            with st.expander(f"📌 {titulo_pt}"):
                if 'published' in item:
                    st.caption(f"🕒 {item.published}")
                
                resumo_pt = traduzir(item.get('summary', 'Sem descrição.'))
                st.write(resumo_pt)
                st.markdown(f"[🔗 Notícia Original]({item.link})")
        
        st.write("") # Espaço
    contador += 1
