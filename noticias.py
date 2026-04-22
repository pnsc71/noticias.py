import streamlit as st
import feedparser
from deep_translator import MyMemoryTranslator
import re
import html
from gtts import gTTS
import io

# 1. Configuração da Página
st.set_page_config(page_title="Radar Pro Voice", page_icon="📡", layout="wide")

st.title("📡 Radar Mundial: Portugal & Mundo")

# 2. Funções de Apoio
@st.cache_data(ttl=300) # Reduzi para 5 min para a tradução não "encravar" tanto
def traduzir_pt(texto):
    if not texto: return ""
    try:
        # Limpeza de HTML e símbolos
        texto_limpo = html.unescape(re.sub('<[^<]+?>', '', texto))
        # Tradutor focado em Portugal
        return MyMemoryTranslator(source='en-GB', target='pt-PT').translate(texto_limpo)
    except:
        return texto

def gerar_audio(texto):
    # gTTS configurado para Português de Portugal
    tts = gTTS(text=texto, lang='pt', tld='pt')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0) # CRUCIAL para o iPhone reconhecer o início do ficheiro
    return fp

# 3. Definição das Fontes
fontes = [
    {"nome": "CNN Portugal", "url": "https://cnnportugal.iol.pt/rss", "cor": "🔴", "traduzir": False},
    {"nome": "RTP Notícias", "url": "https://www.rtp.pt/noticias/rss", "cor": "🔵", "traduzir": False},
    {"nome": "Pplware", "url": "https://pplware.sapo.pt/feed/", "cor": "🟢", "traduzir": False},
    {"nome": "CNN (EUA)", "url": "http://rss.cnn.com/rss/edition.rss", "cor": "🇺🇸", "traduzir": True},
    {"nome": "BBC (UK)", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "cor": "🇬🇧", "traduzir": True},
    {"nome": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml", "cor": "🌍", "traduzir": True}
]

# 4. Barra Lateral com Resumo de Voz
with st.sidebar:
    st.header("🤖 Briefing de Voz")
    st.write("Clica abaixo para ouvir as notícias.")
    
    if st.button("🔊 Gerar Áudio"):
        with st.spinner("A preparar o áudio..."):
            resumo_texto = "Olá Pedro! Aqui tens o teu radar. "
            # Puxa os 4 primeiros títulos para o áudio
            for fonte in fontes[:4]:
                feed = feedparser.parse(fonte['url'])
                if feed.entries:
                    t = feed.entries[0].title
                    t_pt = traduzir_pt(t) if fonte['traduzir'] else html.unescape(t)
                    resumo_texto += f"Na {fonte['nome']}, destaca-se: {t_pt}. "
            
            audio_data = gerar_audio(resumo_texto)
            # Mostra o leitor de áudio
            st.audio(audio_data, format='audio/mp3')
            st.success("Pronto! Clica no Play.")

    st.divider()
    st.info("No iPhone: Se não ouvires, verifica se o botão lateral do silêncio está ligado!")

# 5. Grelha de Notícias
col1, col2 = st.columns(2)
for i, fonte in enumerate(fontes):
    coluna = col1 if i % 2 == 0 else col2
    with coluna:
        st.subheader(f"{fonte['cor']} {fonte['nome']}")
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
                st.caption(f"🔗 [Ler notícia]({item.link})")
        st.write("---")
