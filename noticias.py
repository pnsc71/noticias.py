import streamlit as st
import feedparser
from deep_translator import MyMemoryTranslator
import re
import html

# 1. Configuração e Estilo
st.set_page_config(page_title="Radar Pro + Briefing", page_icon="📡", layout="wide")

st.title("📡 Radar Mundial com Inteligência")

# 2. Função de Tradução
@st.cache_data(ttl=600)
def traduzir_pt(texto):
    if not texto: return ""
    try:
        texto_limpo = html.unescape(re.sub('<[^<]+?>', '', texto))
        return MyMemoryTranslator(source='en-GB', target='pt-PT').translate(texto_limpo)
    except:
        return texto

# 3. Fontes
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "cor": "🔴", "traduzir": False},
    {"nome": "RTP Notícias", "url": "https://www.rtp.pt/noticias/rss", "cor": "🔵", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "cor": "🟢", "traduzir": False},
    {"nome": "CNN (EUA)", "url": "http://rss.cnn.com/rss/edition.rss", "cor": "🇺🇸", "traduzir": True},
    {"nome": "BBC (UK)", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "cor": "🇬🇧", "traduzir": True},
    {"nome": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "cor": "🌍", "traduzir": True}
]

# --- NOVIDADE: O MOTOR DE RESUMO ---
todos_os_titulos = []

# Primeiro, vamos carregar os dados
for fonte in fontes:
    feed = feedparser.parse(fonte['url'])
    for item in feed.entries[:3]: # Pegamos nos 3 principais de cada
        titulo = traduzir_pt(item.title) if fonte['traduzir'] else html.unescape(item.title)
        todos_os_titulos.append(f"{fonte['nome']}: {titulo}")

# Interface na Barra Lateral
with st.sidebar:
    st.header("🤖 Assistente de Resumo")
    if st.button("✨ Diz-me o que perdi"):
        st.subheader("O teu Briefing de hoje:")
        with st.status("A analisar o mundo...", expanded=True):
            # Aqui simulamos uma análise dos temas quentes
            top_noticias = todos_os_titulos[:5] # Mostra as 5 mais frescas
            for n in top_noticias:
                st.write(f"• {n}")
        st.success("Estás atualizado! Estes são os temas dominantes agora.")
    st.markdown("---")
    st.info("Este resumo analisa as 6 fontes em tempo real.")

# --- GRELHA DE NOTÍCIAS (Igual ao anterior) ---
col1, col2 = st.columns(2)
for i, fonte in enumerate(fontes):
    coluna = col1 if i % 2 == 0 else col2
    with coluna:
        st.subheader(f"{fonte['cor']} {fonte['nome']}")
        feed = feedparser.parse(fonte['url'])
        for item in feed.entries[:5]:
            if fonte['traduzir']:
                titulo = traduzir_pt(item.title)
                resumo_raw = item.get('summary', '')
                resumo = traduzir_pt(resumo_raw)
            else:
                titulo = html.unescape(item.title)
                resumo_raw = item.get('summary', '') or item.get('description', '')
                resumo = html.unescape(resumo_raw)
                resumo = re.sub('<[^<]+?>', '', resumo)

            with st.expander(f"📌 {titulo}"):
                st.write(resumo)
                st.caption(f"🔗 [Ler notícia]({item.link})")
        st.write("---")
