import streamlit as st
import feedparser
from deep_translator import GoogleTranslator

# 1. Configuração da Página
st.set_page_config(page_title="Radar Mundial Traduzido", page_icon="🌍", layout="wide")

st.title("🌍 Radar Global: Tradução em Tempo Real")
st.markdown("_As notícias do mundo, traduzidas automaticamente para si._")
st.markdown("---")

# 2. Fontes Internacionais (Inglês)
fontes = {
    "CNN Internacional (EUA)": "http://rss.cnn.com/rss/edition.rss",
    "BBC World News (UK)": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Al Jazeera (Mundo)": "https://www.aljazeera.com/xml/rss/all.xml",
    "RTP Notícias (PT)": "https://www.rtp.pt/noticias/rss" # Para comparar
}

# 3. Função de Tradução
def traduzir_texto(texto):
    try:
        # Traduz do inglês (auto) para o português
        traducao = GoogleTranslator(source='auto', target='pt').translate(texto)
        return traducao
    except:
        return texto # Se falhar, mostra o original

# 4. Grelha de exibição
col1, col2 = st.columns(2)
contador = 0

for nome, url in fontes.items():
    coluna_atual = col1 if contador % 2 == 0 else col2
    
    with coluna_atual:
        st.subheader(f"🗞️ {nome}")
        feed = feedparser.parse(url)
        noticias = feed.entries[:5]
        
        for item in noticias:
            with st.expander(f"📌 {traduzir_texto(item.title)}"):
                st.caption(f"🕒 {item.get('published', '')}")
                
                # Traduzimos o resumo
                resumo_original = item.get('summary', '')
                if resumo_original:
                    resumo_pt = traduzir_texto(resumo_original)
                    st.markdown(resumo_pt, unsafe_allow_html=True)
                
                st.markdown(f"**[🔗 Link Original]({item.link})**")
        st.markdown("---")
    
    contador += 1

st.sidebar.info("💡 Nota: A tradução é feita automaticamente via Google Translator.")
