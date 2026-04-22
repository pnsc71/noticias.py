import streamlit as st
import feedparser
from deep_translator import GoogleTranslator
import re

# 1. Configuração
st.set_page_config(page_title="Radar Mundial pt-PT", page_icon="📡", layout="wide")

# 2. Dicionário de "Tradução" BR -> PT
# Podes adicionar aqui mais palavras que te irritem!
DICIONARIO_PT = {
    "usuário": "utilizador",
    "celular": "telemóvel",
    "tela": "ecrã",
    "trem": "comboio",
    "esporte": "desporto",
    "equipe": "equipa",
    "café da manhã": "pequeno-almoço",
    "gramado": "relvado"
}

def corrigir_sotaque(texto):
    for br, pt in DICIONARIO_PT.items():
        # Substitui ignorando se é maiúscula ou minúscula
        padrao = re.compile(re.escape(br), re.IGNORECASE)
        texto = padrao.sub(pt, texto)
    return texto

@st.cache_data(ttl=600)
def traduzir(texto):
    if not texto: return ""
    try:
        texto_limpo = re.sub('<[^<]+?>', '', texto)
        # Tradução base
        traducao = GoogleTranslator(source='auto', target='pt').translate(texto_limpo)
        # Aplica o nosso filtro de Portugal
        return corrigir_sotaque(traducao)
    except:
        return texto

# --- O resto do código (Dashboard) ---
st.title("📡 Radar Mundial: Sotaque de Portugal")

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
            with st.expander(f"📌 {traduzir(item.title)}"):
                st.write(traduzir(item.get('summary', '')))
                st.markdown(f"[🔗 Original]({item.link})")
